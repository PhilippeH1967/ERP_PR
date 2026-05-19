# Contexte d'audit (3/3) — ordre d'exécution, unicité assoc, SSO, refresh

> Suite de `01-tenant-auth-core.md` + `02-jwt-rls-settings.md`. Skill
> `audit-context-building` (pure-contexte). Résout les 4 items « Reste à
> micro-analyser ». AUCUN finding/fix/sévérité — compréhension uniquement.
> Inclut une **correction** d'un énoncé inexact de `02` (I-trust / refresh).

## Q1 — Une requête DB tenant-scoped peut-elle partir AVANT la vérif JWT ?

Réponse : **non, pour le code actuel**. Chaîne établie :

1. `TenantMiddleware.__call__` (middleware.py L36-95) ne lit **aucune table
   tenant-scoped**. Sa seule requête DB est `Tenant.objects.get(pk=, is_active=True)`
   (L73) → `core_tenant` HORS RLS (a4 résolu en `02`). Le `SET
   app.current_tenant` (L86-88) précède `get_response` mais n'émet pas de
   lecture RLS lui-même.
2. Le `tenant_id` posé au `SET` provient soit du claim JWT non vérifié
   (L44/L107 `verify=False`), soit du header `X-Tenant-Id` (L48). MAIS il
   est borné par `Tenant.objects.get(...is_active=True)` (L73) : le `SET`
   ne peut cibler qu'un tenant **réel et actif**.
3. Les vues s'exécutent APRÈS la couche DRF : `JWTAuthentication`
   (signature vérifiée) → permissions → view. La première lecture
   tenant-scoped est dans le queryset de la vue ⇒ nécessairement APRÈS
   vérif signature. Token forgé ⇒ DRF 401 **avant** que le queryset ne
   parte ⇒ le `SET` (vers un tenant réel mais non autorisé) reste sans
   effet de données (aucune lecture RLS émise).
4. Endpoints publics qui court-circuitent l'auth : `auth_config`
   (auth.py L417-431, `@authentication_classes([])` + `AllowAny`) ne lit
   que `settings.SOCIALACCOUNT_PROVIDERS`, **zéro requête tenant-scoped**,
   et `/api/v1/auth/` est dans `TENANT_EXEMPT_PATHS` ⇒ pas de `SET` du tout.

**Conclusion (ordre prouvé pour le code actuel)** : aucune lecture
tenant-scoped ne peut précéder la vérif signature JWT. I1 (ordre) tenu —
*sous réserve* qu'aucune vue exemptée/`AllowAny` future ne lise une table
RLS (anchor déjà noté, `02` cluster #3).

Note PG : `SET` (pas `SET LOCAL`) n'est PAS annulé par le rollback
`ATOMIC_REQUESTS`. Inoffensif ici car le middleware réécrit le `SET` à
CHAQUE requête non-exempte (L86-88) et les exemptes ne lisent pas de RLS.
Redevient pertinent uniquement si pgbouncer transaction s'intercale (a3).

## Q2 — `UserTenantAssociation` : un user peut-il en avoir plusieurs ?

Réponse : **non, structurellement impossible**. `user =
models.OneToOneField(...)` (models.py L151) ⇒ contrainte UNIQUE DB sur
`user_id`. Un user a **au plus une** association.

- `user.tenant_association` (auth.py L38-39, L102-103) est déterministe
  (objet unique ou `RelatedObjectDoesNotExist`, capturé par
  `contextlib.suppress`).
- Tous les points de création passent par `get_or_create` /
  `ensure_user_tenant_association` (signals.py L31-35, auth.py L211,
  import commands) — aucun chemin ne crée un 2e lien.
- Renforce **a5** (un tenant par requête) au niveau user, et **I-trust**
  (source unique du claim `tenant_id`).

## Q3 — Flux SSO (allauth) : comment le tenant est-il résolu ?

Mécanique (signals.py + base.py L353-389) :
- Provider unique : **Microsoft Entra ID OIDC** (activé seulement si
  `ENTRA_CLIENT_ID`+`ENTRA_TENANT_ID` en env ; sinon `SOCIALACCOUNT_PROVIDERS={}`).
- `SOCIALACCOUNT_AUTO_SIGNUP=True` + `SOCIALACCOUNT_EMAIL_AUTHENTICATION=True`
  ⇒ user auto-créé au 1er login SSO.
- `@receiver(social_account_added)` → `ensure_user_tenant_association(user)`
  → `get_or_create_default_tenant()` : **slug `"default"` en dur**.

**Observation de contexte majeure** : la résolution SSO mappe **TOUS** les
users SSO vers le **MÊME** tenant `"default"`. Aucune dérivation
per-organisation depuis les claims OIDC (tenant Entra, domaine email…).
Cohérent pour un déploiement mono-org (Provencher Roy). L'infra RLS est
multi-tenant mais le **provisioning SSO est mono-tenant** ⇒ anchor de
divergence infra↔intention si le multi-org SSO est un jour visé. (Contexte,
pas finding.)

Sous-cas fail-closed : si un flux crée l'user sans déclencher
`social_account_added` (le receiver n'écoute QUE ce signal), l'association
peut manquer ⇒ `token.tenant_id=None` ⇒ RLS bloque dur (I1). Cohérence
fail-closed d'ensemble préservée.

## Q4 — Refresh token : recharge-t-il tenant/roles ou recopie l'ancien claim ?

Réponse : **recopie l'ancien claim, NE recharge PAS depuis la DB**.
**→ Ceci CORRIGE `02` L101-102 (« refresh régénère par la même voie » est INEXACT).**

Mécanique (auth.py L89-92 + SIMPLE_JWT base.py L392-401) :
- `CustomTokenRefreshView(TokenRefreshView): pass` — n'override PAS
  `serializer_class` ⇒ `TokenRefreshSerializer` par défaut.
- `CustomTokenObtainPairSerializer.get_token` (L28-52) ajoute `email`,
  `tenant_id`, `roles[]` sur le `RefreshToken` retourné par
  `super().get_token(user)` ⇒ ces claims custom sont **sur le refresh token**.
- Au refresh, `TokenRefreshSerializer` fait `RefreshToken(refresh).access_token` :
  cette propriété **copie tous les claims non-registered** du payload
  refresh vers le nouvel access token. `get_token(user)` n'est **jamais**
  rappelé ⇒ `tenant_id`/`roles`/`email` **figés à la 1re émission (login)**,
  propagés tels quels.
- `ROTATE_REFRESH_TOKENS=True` + `BLACKLIST_AFTER_ROTATION=False`
  (L395-396) : la rotation réémet un refresh en **réutilisant le même
  payload** (nouveaux `jti`/`exp`/`iat` seulement). Les claims custom
  persistent à travers toutes les rotations, sans re-dérivation DB, tant
  que l'user refresh dans la fenêtre (`REFRESH_TOKEN_LIFETIME=7j`, repoussée
  à chaque rotation). Anciens refresh non blacklistés (contexte, pas finding).

Portée de la péremption (bornée) :
- **roles[]** : staleness sans impact — l'autorité reste `ProjectRole`
  requêtée à chaque requête par les permissions DRF (**I-roles**, `02`
  L103-104). Révocation de rôle toujours immédiate côté autorisation.
- **tenant_id** : utilisé par le middleware pour le `SET`. Borné car
  `UserTenantAssociation` est OneToOne créé une fois (Q2). Si un admin
  change `UserTenantAssociation.tenant`, les tokens existants gardent
  l'ancien `tenant_id` jusqu'à re-login complet — **fenêtre de staleness
  connue**, pas une fuite (RLS + `Tenant.objects.get(is_active=True)`
  revalident à chaque requête ; `tenant_id` ∈ {None, tenant réel actif}).

## Invariants — mise à jour

- **I-trust (CORRIGÉ)** : `token.tenant_id` provient de
  `UserTenantAssociation` **uniquement à la 1re émission (login)** ; figé
  et **recopié à l'identique par CHAQUE refresh/rotation** (PAS régénéré).
  Fenêtre de staleness = durée de vie de la chaîne de refresh (≥7j si
  l'user refresh régulièrement). Borné par OneToOne (Q2) + revalidation
  RLS/Tenant par requête.
- **I-roles** : confirmé — claim `roles[]` purement informatif, autorité
  DB live à chaque requête (vrai aussi après refresh, vu Q4).
- **I1 (ordre)** : prouvé pour le code actuel (Q1) — aucune lecture
  tenant-scoped avant vérif signature JWT.
- **I-assoc (nouveau)** : `UserTenantAssociation` est OneToOne ⇒ ≤1 par
  user, garanti DB. Source unique de `tenant_id`.

## Clusters de fragilité — actualisés (orientation, PAS findings)

1. ~~SET ↔ pgbouncer~~ levé infra actuelle (anchor a3 si pgbouncer txn ajouté).
2. Claim JWT non vérifié pour le SET → atténué par I1 ordre (Q1) + RLS
   fail-closed.
3. Exemption `startswith` + `/admin/` vs `/django-admin/` — anchor cohérence.
4. `validate()` sso_only fail-open si assoc manquante — cohérent (RLS bloque).
5. **(nouveau)** Provisioning SSO mono-tenant `"default"` en dur vs infra
   RLS multi-tenant — anchor de divergence si multi-org SSO visé.
6. **(nouveau)** Staleness `tenant_id` à travers refresh/rotation (Q4) —
   bornée, à garder en tête lors d'un futur audit du flux de changement
   d'organisation d'un user.

## Statut global du contexte d'audit

Contexte consolidé **complet** pour le cœur isolation tenant + auth :
les hypothèses ouvertes (a1–a5, a-hdr, a-jwt1/2, I-trust, I1, I4) sont
résolues ou ancrées. Les 6 clusters de fragilité sont des **orientations
pour une phase ultérieure** (findings/fix hors scope du skill pure-contexte).
