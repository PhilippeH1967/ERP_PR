# Audit — Findings & remédiation (isolation tenant + auth)

> Phase post pure-contexte (demandée explicitement). S'appuie sur `01`→`03`.
> Sévérités : CRITIQUE / ÉLEVÉ / MOYEN / FAIBLE. Chaque finding : cause
> racine → impact → exploit → correctif.

---

## F1 — CRITIQUE — RLS totalement inerte en production

**Cause racine.** `setup_rls.py` L50 fait `ALTER TABLE … ENABLE ROW LEVEL
SECURITY` mais **jamais `FORCE ROW LEVEL SECURITY`**. Django se connecte
avec `POSTGRES_USER` (`erp_user`, base.py L201 / docker-compose.prod.yml
L65). Les migrations créent les tables sous ce même rôle ⇒ **`erp_user`
est PROPRIÉTAIRE des tables**. En PostgreSQL, le propriétaire d'une table
est **exempté des policies RLS** sauf si `FORCE ROW LEVEL SECURITY` est
positionné.

**Impact.** L'isolation multi-tenant au niveau base de données est **nulle**
en production. La propriété « fail-closed dur, aucune fuite cross-tenant
silencieuse » documentée en `02`/`03` (I1) est **FAUSSE pour la connexion
applicative** : `current_setting('app.current_tenant')` n'est jamais
évalué pour le propriétaire. Toute la séparation repose sur les ~42
filtres applicatifs `get_queryset` dont l'uniformité n'est PAS prouvée
(`02` §"Pattern get_queryset"). Un seul oubli — viewset, `objects.all()`
dans un service/rapport, tâche Celery, agrégat dashboard, `RawSQL` —
retourne ou écrit des données d'un autre tenant, sans aucun filet PG.

**Exploit.** Tout chemin de code tenant-scoped ne filtrant pas
explicitement `tenant_id` traverse les tenants. Combiné à F3 (header
`X-Tenant-Id`) : un utilisateur authentifié sans claim tenant force
n'importe quel tenant et lit/écrit ses données.

**Correctif (défense en profondeur, 2 niveaux) :**

1. **`FORCE` immédiat** dans `setup_rls.py` :
   ```python
   cursor.execute(f"ALTER TABLE {quoted_table} ENABLE ROW LEVEL SECURITY;")
   cursor.execute(f"ALTER TABLE {quoted_table} FORCE ROW LEVEL SECURITY;")
   ```
2. **Rôle applicatif non-propriétaire** (cible) : créer `erp_app` (NOLOGIN
   superuser, NOBYPASSRLS) propriétaire des tables = rôle de migration ;
   `erp_app_rw` (connexion Django) avec uniquement `SELECT/INSERT/UPDATE/
   DELETE`. RLS s'applique alors même sans `FORCE`, et `FORCE` reste un
   garde-fou.
3. **Test d'intégration RLS** (TDD, manquant) : sous `app.current_tenant=A`,
   une requête sur des données du tenant B doit retourner 0 ligne / lever.
   À exécuter avec une connexion **non-propriétaire** (sinon le test passe
   à tort, masquant F1 — piège actuel des tests).
4. Garder `current_setting(...)` **sans** `, true` (fail-closed) — déjà OK.

---

## F2 — ÉLEVÉ — Endpoints admin `user_*` non scoping tenant

**Cause racine.** `auth.py` `user_delete`/`user_update`/`user_create`/
`user_list` opèrent sur `User.objects.get(pk=pk)` / `User.objects.all()`
(modèle Django `User`, **hors RLS**). `IsAdmin` vérifie que l'appelant est
admin, **jamais** que l'utilisateur cible appartient au tenant de
l'appelant. `user_update` L162 et `user_create` L209 assignent rôle /
association via `Tenant.objects.first()` (tenant arbitraire).

**Impact / exploit.** Un ADMIN du tenant A énumère les `pk`, **réinitialise
les mots de passe**, (dés)active des comptes, change les rôles
d'utilisateurs du tenant B ; les nouveaux users sont rattachés au
« premier » tenant. Prise de contrôle cross-tenant via la gestion des
utilisateurs. Exploitable indépendamment de F1.

**Correctif.** Scoper toutes les requêtes `user_*` par
`UserTenantAssociation.tenant_id == request.tenant_id` ; remplacer
`Tenant.objects.first()` par `request.tenant`. Refuser si la cible n'est
pas dans le tenant de l'appelant (404, pas 403, pour ne pas révéler
l'existence). Tests permissions cross-tenant obligatoires.

---

## F3 — ÉLEVÉ — Fallback `X-Tenant-Id` actif en production

**Cause racine.** `middleware.py` L47-48 : si le JWT n'a pas de claim
`tenant_id`, le tenant est lu depuis l'en-tête client `X-Tenant-Id`
(commentaire « development/testing »), sans aucune garde d'environnement.

**Impact / exploit.** Tout utilisateur authentifié dont le token n'a pas
de `tenant_id` (user sans `UserTenantAssociation` — cf. F6) envoie
`X-Tenant-Id: <tenant cible>`. Le middleware valide le tenant et pose le
`SET`. Avec F1 (RLS inerte) : lecture/écriture cross-tenant directe sur
tout endpoint `IsAuthenticated`.

**Correctif.** Conditionner le fallback à `settings.DEBUG` (ou un flag
explicite `TENANT_HEADER_FALLBACK`), jamais en prod :
```python
if tenant_id is None and settings.DEBUG:
    tenant_id = request.headers.get("X-Tenant-Id")
```
Cible : ne dériver le tenant que d'une source serveur de confiance
(cf. F4).

---

## F4 — MOYEN — Tenant dérivé d'un JWT non vérifié pour le `SET`

**Cause racine.** `middleware.py` L107 `AccessToken(token_str,
verify=False)` : le claim `tenant_id` qui pilote le `SET app.current_tenant`
n'est pas signature-vérifié au moment du SET (DRF re-vérifie plus tard).

**Impact.** Atténué quand RLS fonctionne (fail-closed) + DRF rejette le
token forgé en 401 avant la vue. Mais le `SET` a lieu inconditionnellement ;
fragile dès qu'un endpoint `AllowAny` touche du tenant-scoped (aucun
aujourd'hui — `auth_config`/`api_root`/`health_check` ne lisent rien de
tenant — mais sans garde structurelle).

**Correctif (cible).** Dériver le tenant **après** l'auth DRF depuis
`request.user.tenant_association.tenant_id` (source serveur unique,
OneToOne — `I-assoc`), pas depuis le claim client. Alternative court
terme : `verify=True` dans le middleware avec la clé de signing.

---

## F5 — MOYEN — Révocation de refresh token faible

**Cause racine.** base.py L395-396 : `ROTATE_REFRESH_TOKENS=True` +
`BLACKLIST_AFTER_ROTATION=False`, et l'app `token_blacklist` n'est pas
installée. Claims figés au 1er login et recopiés (`03` Q4).

**Impact.** Un refresh token volé/fuité reste valide jusqu'à expiration
naturelle (7 j) ; un re-login légitime ne l'invalide pas. Atténué :
access 15 min, simplejwt vérifie `user.is_active` à chaque requête
(compte désactivé bloqué immédiatement).

**Correctif.** `BLACKLIST_AFTER_ROTATION=True` + ajouter
`rest_framework_simplejwt.token_blacklist` à `INSTALLED_APPS` + migrate ;
endpoint logout qui blackliste le refresh.

---

## F6 — MOYEN — `sso_only` fail-open si association manquante

**Cause racine.** `auth.py` L77-78 `except Exception: pass` : si
`tenant_association` manque, le contrôle `sso_only` est court-circuité
(login mot de passe autorisé).

**Impact.** Un user non-ADMIN sans association sur un tenant `sso_only`
se connecte par mot de passe (politique SSO contournée). Compose avec
F3 (pas d'association ⇒ fallback header) + F1.

**Correctif.** Fail-closed : distinguer « association absente » (refuser
le login non-ADMIN, ou exiger l'association) des erreurs réellement
inattendues. Ne pas avaler `RelatedObjectDoesNotExist` en autorisation.

---

## F7 — FAIBLE — `TENANT_EXEMPT_PATHS` désaligné

`/admin/` exempté (devenu SPA Vue, config morte) ; `/django-admin/`
(vrai admin Django, commit e9432a5) **non** exempté ⇒ admin Django
(session, sans JWT) ⇒ `tenant=None`. Avec F1 il voit tout ; RLS forcé
le casserait fonctionnellement (admin ne liste plus aucun modèle
tenant-scoped). **Correctif.** Aligner les paths ; stratégie RLS explicite
pour `/django-admin/` (rôle `BYPASSRLS` dédié au superuser, ou set tenant
explicite côté admin).

---

## F8 — FAIBLE — Provisioning SSO mono-tenant en dur

`signals.py` `get_or_create_default_tenant()` slug `"default"`. Sans
impact pour le déploiement mono-org (Provencher Roy). **Correctif
préventif.** Avant tout SSO multi-org : résoudre le tenant depuis
l'issuer OIDC / domaine email ; ajouter une assertion documentant
l'hypothèse mono-org.

---

## Plan de remédiation (ordre recommandé)

| # | Sévérité | Effort | Dépend de |
|---|---|---|---|
| F1 | CRITIQUE | M (FORCE) → L (rôle non-owner) | — |
| F2 | ÉLEVÉ | M | — |
| F3 | ÉLEVÉ | S | — |
| F6 | MOYEN | S | — |
| F5 | MOYEN | M (app blacklist + migration) | — |
| F4 | MOYEN | M | F3 |
| F7 | FAIBLE | S | F1 |
| F8 | FAIBLE | S (préventif) | — |

**F1 d'abord** : il transforme F2/F3/F6 de « grave » en « défense en
profondeur ». Chaque correctif suit le TDD imposé (test rouge → code →
vert), avec tests de permission cross-tenant et un **test d'intégration
RLS exécuté sous une connexion non-propriétaire**.
