# Contexte d'audit (2/2) — JWT claims, RLS, settings (pure-contexte)

> Suite de `01-tenant-auth-core.md`. Skill `audit-context-building`.
> Résout les hypothèses ouvertes a3, a4, I1, I-trust. AUCUN finding/fix.

## Micro-analyse `CustomTokenObtainPairSerializer` (auth.py L25-80)

Purpose : maillon de confiance — injecte `tenant_id`, `email`, `roles[]` dans
le JWT d'accès à l'émission (login) et au refresh.

`get_token` (L28-52) bloc par bloc :
- L33 `token["email"] = user.email`.
- L36-40 : `tenant_id` lu depuis `user.tenant_association.tenant_id`, entouré
  de `contextlib.suppress(Exception)` → si pas d'association ⇒ `tenant_id=None`.
  **Résout I-trust** : la source unique du claim tenant est
  `UserTenantAssociation` au moment de l'émission. Figé dans le token jusqu'au
  refresh (qui re-passe par `get_token`). a2 confirmée : claim fiable car posé
  serveur depuis une FK, jamais depuis une entrée client.
- L43-50 : `roles[]` = liste `{project_id, role}` depuis `ProjectRole`.
  Couplage : les permissions DRF (`is_admin`, etc.) requêtent `ProjectRole`
  en direct (pas le claim) → le claim roles[] est informatif/UI, l'autorité
  reste la DB à chaque requête (bon : révocation de rôle immédiate).
- Invariant I-trust : `token.tenant_id ∈ {None, UserTenantAssociation.tenant_id}`.

`validate` (L54-80) :
- Bloque login local si `tenant.sso_only` (sauf rôle ADMIN).
- L77-78 `except Exception: pass` : si l'association manque, le contrôle
  sso_only est court-circuité (fail vers login autorisé). *Observation de
  contexte* : un user sans `tenant_association` n'est jamais bloqué par
  sso_only ET aura `token.tenant_id=None` ⇒ ne résoudra aucun tenant au
  middleware ⇒ RLS le bloque dur (voir I1 ci-dessous). Cohérence d'ensemble
  fail-closed, à garder en tête (pas un finding).

## Micro-analyse `setup_rls.py` (RÉSOUT a4 + I1)

- L26-32 : cible tout modèle `issubclass(TenantScopedModel)`, non abstract,
  managed. **`class Tenant(models.Model)` (models.py L12) N'hérite PAS de
  TenantScopedModel** → `core_tenant` n'a PAS de policy RLS.
  **a4 RÉSOLU** : `Tenant.objects.get(pk=tenant_id)` au middleware L73 ne
  dépend pas de `app.current_tenant` ⇒ aucune récursion poule-œuf. I confirmé.
- L55-63 : policy `tenant_isolation` =
  `USING (tenant_id = current_setting('app.current_tenant')::int)`
  `WITH CHECK (même condition)`.
  - `USING` filtre les SELECT/UPDATE/DELETE.
  - `WITH CHECK` empêche INSERT/UPDATE de poser un `tenant_id` ≠ courant
    (couplage écriture protégé).
  - **Point majeur (raffine I1)** : `current_setting('app.current_tenant')`
    est appelé SANS le 2e argument `, true` (missing_ok). Si la variable
    n'est pas définie sur la connexion, PostgreSQL lève une **erreur** au
    lieu de retourner NULL. Conséquence : une requête sur une table RLS
    **sans `SET` préalable échoue dur (fail-closed)** — il ne peut PAS y
    avoir de fuite cross-tenant par "SET manquant" (la requête plante).
    C'est une propriété de sûreté forte du design.
- L43 : `transaction.atomic()` + rollback global si une seule policy échoue
  (idempotent, tout-ou-rien).

## Micro-analyse settings (RÉSOUT a3 pour l'infra actuelle)

- `MIDDLEWARE` (base.py L163-176) : `TenantMiddleware` (L170) AVANT
  `AuthenticationMiddleware` (L171). L'auth DRF/JWT s'exécute encore plus
  tard (couche view). ⇒ le `SET app.current_tenant` précède l'authentification
  ⇒ confirme la dépendance a-jwt2 (claim lu non vérifié pour le SET).
- `DATABASES` (L200-211) : `ATOMIC_REQUESTS=True` (1 transaction / requête
  HTTP), `CONN_MAX_AGE=600` (connexions Django persistantes 10 min).
- `production.py` ne redéfinit PAS `DATABASES` ⇒ hérite de base.py.
- `docker-compose.prod.yml` : **service `postgres` direct (port 5432), AUCUN
  service pgbouncer**. Le `CLAUDE.md` racine mentionne "PostgreSQL 16
  (pgbouncer pool)" mais l'infra Docker prod actuelle n'embarque PAS de
  pgbouncer. **a3 RÉSOLU pour l'état actuel** : Django parle directement à
  PostgreSQL. Connexion persistante par worker (CONN_MAX_AGE), le `SET`
  session est réécrit à CHAQUE requête non-exempte (middleware L86-88) ⇒
  pas de fuite par connexion réutilisée tant qu'aucun pooler transaction
  ne s'intercale.
  - **Anchor de divergence doc↔infra** : si pgbouncer est ajouté plus tard
    en mode `transaction`, a3 redevient critique (le `SET` session ne
    survivrait pas au changement de connexion entre transactions) — à
    réévaluer le jour où pgbouncer est introduit. (Contexte, pas finding.)

## Pattern `get_queryset` tenant-filtré (défense applicative)

- ~42 `def get_queryset` dans `apps/*/views.py`, ~53 lignes filtrant
  explicitement `tenant`/`tenant_id`. Défense **applicative en plus de RLS**
  (defense-in-depth). L'uniformité exacte n'est pas garantie sans inspection
  exhaustive de chaque viewset, MAIS le filet PG (RLS fail-closed via I1)
  reste la garantie de plus bas niveau : même un viewset oubliant le filtre
  applicatif ne peut pas retourner de données d'un autre tenant (RLS bloque
  ou plante). À micro-analyser viewset par viewset lors d'une phase ultérieure
  si l'on veut prouver l'uniformité applicative.

## Invariants consolidés (statuts mis à jour)

- **I1** (raffiné, RÉSOLU au niveau design) : toute requête sur une table
  tenant-scoped opère sous `app.current_tenant` correct OU échoue
  (fail-closed dur, `current_setting` sans missing_ok). Pas de fuite
  silencieuse possible par SET manquant. *Réserve : valable tant qu'aucun
  pgbouncer transaction-pooling n'est intercalé (a3).*
- **I2** : `request.tenant_id ∈ {None, int Tenant actif}`. Tenu.
- **I4** : désactivation Tenant effective requête suivante (middleware L73,
  Tenant hors RLS donc lisible). Tenu.
- **I-trust** (RÉSOLU — ⚠️ raffiné/corrigé dans `03` Q4) : `token.tenant_id`
  vient uniquement de `UserTenantAssociation` à l'émission. *Énoncé initial
  « refresh régénère par la même voie » INEXACT* : le refresh **recopie**
  l'ancien claim (pas de re-dérivation DB). Voir `03` pour la version
  corrigée et la fenêtre de staleness bornée.
- **I-roles** (nouveau) : l'autorité des rôles est `ProjectRole` requêtée à
  chaque requête (claim roles[] = cache informatif) ⇒ révocation immédiate.

## Clusters de fragilité — statut actualisé (orientation, PAS findings)

1. ~~SET session ↔ pgbouncer~~ → **levé pour l'infra actuelle** (pas de
   pgbouncer). Redevient pertinent si pgbouncer transaction ajouté. Anchor.
2. Claim JWT non vérifié pour le SET (a-jwt2) → atténué par I1 fail-closed :
   un SET issu d'un token forgé non signé ⇒ DRF rejette en 401 avant accès
   données ; et même si une requête DB partait, RLS exige un tenant entier
   valide. Reste à prouver formellement l'ordre middleware→auth→toute requête DB.
3. Exemption `startswith` + incohérence `/admin/`(SPA) vs `/django-admin/`
   (Django) non répercutée dans `TENANT_EXEMPT_PATHS`. Sans effet données
   (SPA ne requête pas la DB) mais anchor de cohérence à corriger un jour.
4. `validate()` sso_only fail-open silencieux si association manquante —
   cohérent avec le reste (user sans tenant ⇒ RLS le bloque), à garder
   en tête lors d'un futur audit du flux SSO.

## Reste à micro-analyser (si poursuite)
- Ordre exact d'exécution : peut-il partir une requête DB tenant-scoped
  AVANT la vérif JWT DRF ? (inspection des middlewares aval + DRF auth flow).
- `UserTenantAssociation` : un user peut-il en avoir plusieurs ? unicité ?
- Flux SSO (`allauth`) : comment le tenant est-il résolu côté SSO ?
- Refresh token : `CustomTokenObtainPairView` + `TokenRefreshView` — le
  refresh recharge-t-il tenant/roles à jour ou recopie l'ancien claim ?
