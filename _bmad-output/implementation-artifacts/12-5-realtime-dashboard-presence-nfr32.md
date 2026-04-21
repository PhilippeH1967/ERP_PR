# Story 12.5: Real-Time Dashboard & Presence Indicators (NFR32) — MVP-1

Status: draft

## Story
As a **PM, Associé en charge, Finance user or BU Director**, I want the project dashboards (KPIs + alerts) and the sensitive financial edit screens (invoice preparation, project budget) to update in real time via WebSocket, And I want a presence indicator showing *"En cours d'édition par [utilisateur]"* when another user is editing the same financial record, So that I have immediate feedback and avoid silent conflicts.

## Context
- **NFR32 (MVP-1, confirmé par Philippe 2026-04-21)** covers two distinct capabilities :
  1. **Real-time dashboard updates** — KPI cards, alerts, pipeline numbers push-updated on mutations (architecture.md §129, epics.md L845/1376/1419)
  2. **Presence indicator** — "En cours d'édition par [utilisateur] — dernière activité il y a XXs" on invoice preparation + project budget screens (prd.md NFR32, architecture.md L413-418)
- Current reality :
  - `uvicorn` ASGI server présent ([backend/requirements/base.txt:16](../../backend/requirements/base.txt#L16))
  - `channels` / `channels-redis` **non installés**
  - [backend/config/asgi.py](../../backend/config/asgi.py) minimal (pas de `ProtocolTypeRouter`)
  - Aucun consumer Channels existant
  - `backend/apps/dashboards/` expose REST uniquement ([backend/apps/dashboards/views.py](../../backend/apps/dashboards/views.py))
  - Redis 7 déjà en prod (Docker Compose) — channel layer réutilisable
- Architecture décisions déjà actées (architecture.md §Real-Time Presence) :
  - WebSocket channel **par écran** financier
  - Heartbeat **30s**, timeout **60s**
  - Message format : `{"type": "presence.update", "payload": {"user": "Nathalie", "screen": "invoice_prep", "project_id": 42}}`
- Reference : `_bmad-output/planning-artifacts/module-projets.md` §9.5, architecture.md §Real-Time Presence.

## Acceptance Criteria

### AC1 — Infrastructure Channels + Redis channel layer
- **Given** le backend Django
- **When** la story est mergée
- **Then** `channels>=4.0` et `channels-redis>=4.0` sont installés
- **And** `config/asgi.py` monte un `ProtocolTypeRouter` exposant `/ws/` routes
- **And** `CHANNEL_LAYERS` configure `channels_redis.core.RedisChannelLayer` avec le Redis existant
- **And** `docker-compose.yml` + `docker-compose.prod.yml` lancent `django` via Uvicorn en mode ASGI (pas gunicorn WSGI)
- **And** un healthcheck WebSocket simple `/ws/ping/` répond `pong`

### AC2 — Authentification WebSocket
- **Given** un WebSocket client
- **When** il tente `wss://.../ws/<route>/` sans token JWT valide
- **Then** la connexion est refusée (close code 4401)
- **And** le middleware d'auth Channels valide le JWT (identique au middleware HTTP) et injecte `user` + `tenant_id` dans `scope`
- **And** les routes WebSocket respectent l'isolement tenant (un user du tenant A ne peut pas subscribe à un canal du tenant B)

### AC3 — Dashboard temps réel (push KPIs)
- **Given** un dashboard ouvert (DashboardView.vue)
- **When** une mutation backend modifie un KPI que le dashboard affiche (facture créée/validée, time entry validé, dépense approuvée, etc.)
- **Then** le consumer `DashboardConsumer` push un event au groupe `dashboard:<tenant_id>:<role>` / `dashboard:<tenant_id>:<user_id>` selon le cas
- **And** le frontend reçoit l'event et met à jour les KPI concernés en ≤ 1s sans refetch HTTP
- **And** des signaux Django (`post_save` sur Invoice, TimeEntry, Expense, STInvoice) déclenchent l'envoi
- **And** en l'absence de WebSocket (fallback), le dashboard continue à fonctionner en mode polling HTTP léger (toutes les 60s)

### AC4 — Presence indicator (invoice prep + project budget)
- **Given** un utilisateur ouvre l'écran **Préparation facture** OU **Budget projet** d'un projet
- **When** il est seul → aucun indicateur visible
- **When** un 2ᵉ utilisateur ouvre le même écran du même projet
- **Then** les deux voient un badge en haut de l'écran : `"En cours d'édition par Nathalie — dernière activité il y a 12s"`
- **And** format : avatar + prénom + timer relatif (fr-CA)
- **And** heartbeat client → serveur toutes les **30s**
- **And** serveur marque la présence **expirée** après **60s** sans heartbeat
- **And** à la fermeture de l'onglet / déconnexion, le serveur diffuse un event `presence.leave` → badge retiré chez les autres
- **And** plusieurs utilisateurs simultanés → badge liste jusqu'à 3 noms, puis `"+ N autres"`

### AC5 — Couverture des écrans MVP-1
NFR32 ciblé MVP-1 couvre **a minima** ces écrans :
- **Écrans avec presence indicator** :
  - Préparation facture (`/billing/invoices/:id/prepare`)
  - Budget projet (onglet Budget de `/projects/:id`)
- **Écrans avec updates temps réel** (KPIs / listes) :
  - Dashboard global (`/dashboard`)
  - Dashboard projet (`/projects/:id` onglet "Dashboard" + KPIs de l'entête)
  - Finance projet (onglet Finance — KPI cashflow + rentabilité, complément story 12.3)

### AC6 — Composable frontend réutilisable
- **Given** la logique WebSocket doit être réutilisable
- **When** un dev crée un nouvel écran nécessitant du real-time
- **Then** un composable `useWebSocket<T>(url, onMessage)` existe dans `frontend/src/shared/composables/`
- **And** le composable gère : connexion initiale, reconnexion exponentielle (1s → 30s max), heartbeat configurable, parsing JSON, typage TypeScript générique
- **And** un composable dédié `usePresence(screen, resourceId)` encapsule l'AC4
- **And** documentation (JSDoc) + 2 exemples d'usage

### AC7 — Déploiement Hostinger
- **Given** le VPS Hostinger
- **When** la story est déployée
- **Then** nginx proxifie `/ws/` vers Django en mode `proxy_http_version 1.1` + `Upgrade` / `Connection` headers
- **And** `docker compose -f docker-compose.prod.yml up -d --build django` utilise uvicorn avec `--workers` et `--ws auto`
- **And** la connexion WebSocket fonctionne via HTTPS (`wss://`) avec le certificat Let's Encrypt existant
- **And** la checklist `_bmad/.../deployment.md` est mise à jour avec les commandes ASGI

### AC8 — Observabilité
- **Given** la prod en fonctionnement
- **When** un incident WebSocket se produit (déconnexions anormales, lag)
- **Then** les logs applicatifs tracent : connexions ouvertes/fermées, user + screen, durées
- **And** pas de données personnelles ni de tokens dans les logs (security.md)
- **And** un endpoint admin `/api/admin/ws-stats/` affiche : connexions actives, par screen, par tenant

## Tasks / Subtasks

### Backend — Infrastructure (Phase 1)
- [ ] **TDD first** — écrire tests de connexion/fermeture/auth échoue avant d'implémenter
- [ ] Ajouter `channels>=4.0` + `channels-redis>=4.0` dans `backend/requirements/base.txt`
- [ ] Mettre à jour `config/asgi.py` avec `ProtocolTypeRouter` + `URLRouter` + `AuthMiddlewareStack`
- [ ] Ajouter `"channels"` dans `INSTALLED_APPS` + `ASGI_APPLICATION = "config.asgi.application"`
- [ ] Configurer `CHANNEL_LAYERS` avec Redis (settings `base.py` et `prod.py`)
- [ ] Créer middleware `JWTAuthMiddleware` pour Channels (compatible simplejwt)
- [ ] Router WebSocket dans nouveau fichier `config/ws_urls.py`

### Backend — Dashboard consumer (Phase 2)
- [ ] `apps/dashboards/consumers.py` : `DashboardConsumer(AsyncJsonWebsocketConsumer)`
- [ ] Groupes : `dashboard:<tenant_id>:<role>` et `dashboard:<tenant_id>:<user_id>`
- [ ] Signals `post_save` sur Invoice, TimeEntry, Expense, STInvoice → `async_to_sync(channel_layer.group_send)` avec payload KPI delta
- [ ] Tests unitaires avec `ChannelsLiveServerTestCase` ou `AsyncHttpClient` — connexion auth, événement reçu après mutation

### Backend — Presence consumer (Phase 3)
- [ ] `apps/core/consumers.py` : `PresenceConsumer(AsyncJsonWebsocketConsumer)`
- [ ] URL : `/ws/presence/<screen>/<resource_id>/` (ex : `/ws/presence/invoice_prep/42/`)
- [ ] Groupe : `presence:<tenant_id>:<screen>:<resource_id>`
- [ ] State stocké en Redis avec TTL 60s (key : `presence:<group>:<user_id>`) pour éviter fuite en cas de crash
- [ ] Heartbeat : message `{"type": "heartbeat"}` toutes les 30s → refresh TTL
- [ ] Broadcast `presence.update` / `presence.leave`
- [ ] Tests : 2 clients, timeout 60s (accéléré en test), expiration → broadcast leave

### Frontend — Composables (Phase 4)
- [ ] `frontend/src/shared/composables/useWebSocket.ts` — générique, reconnexion exponentielle, heartbeat
- [ ] `frontend/src/shared/composables/usePresence.ts` — spécialisé NFR32
- [ ] `frontend/src/shared/composables/useDashboardRealtime.ts` — abonne au canal dashboard
- [ ] Tests Vitest avec mock WebSocket (lib `jest-websocket-mock` ou équivalent Vitest)

### Frontend — Intégration écrans (Phase 5)
- [ ] `DashboardView.vue` : consume `useDashboardRealtime`, update réactif des KPI
- [ ] `ProjectDetail.vue` onglet Finance : idem (complément story 12.3)
- [ ] Écran **Préparation facture** : branche `usePresence('invoice_prep', invoice.id)` + affichage badge
- [ ] `ProjectDetail.vue` onglet **Budget** : branche `usePresence('project_budget', project.id)` + affichage badge
- [ ] Composant `PresenceBadge.vue` dans `shared/components/` (avatar + noms + timer, jusqu'à 3 + "+ N autres")

### Déploiement (Phase 6)
- [ ] Update `docker-compose.yml` et `docker-compose.prod.yml` : commande Django = uvicorn ASGI
- [ ] Update `nginx/nginx.conf` (ou `default.conf`) : `location /ws/` avec `proxy_http_version 1.1`, `Upgrade`, `Connection`
- [ ] Update `.claude/rules/deployment.md` : section ASGI + WebSocket
- [ ] Tests fumée en staging Hostinger : ouvrir 2 onglets, vérifier presence + dashboard real-time
- [ ] Vérifier certificat `wss://` fonctionnel via navigateur

### Documentation (Phase 7)
- [ ] Update `module-projets.md` §9.5 → ✅ livré avec date
- [ ] Update `architecture.md` si design final diffère des décisions initiales
- [ ] Ajouter un ADR court dans `docs/` décrivant le choix Channels vs alternatives (SSE, polling long)

## Tests

### Backend (pytest + pytest-asyncio + Channels)
- [ ] `test_ws_connection_requires_jwt` — close 4401 sans token
- [ ] `test_ws_connection_tenant_isolation` — user tenant A → subscribe tenant B channel → refusé
- [ ] `test_dashboard_consumer_receives_kpi_update_on_invoice_save`
- [ ] `test_dashboard_consumer_group_routing_by_role` — PM voit ses projets, pas ceux d'un autre PM
- [ ] `test_presence_consumer_join_broadcasts_update`
- [ ] `test_presence_consumer_heartbeat_refreshes_ttl`
- [ ] `test_presence_consumer_timeout_60s_triggers_leave_broadcast` — avec TTL accéléré
- [ ] `test_presence_consumer_explicit_close_broadcasts_leave`
- [ ] `test_ws_logs_no_sensitive_data` — vérifier que les tokens/NAS ne sont pas loggés

### Frontend (Vitest + Playwright)
- [ ] Vitest : `useWebSocket` reconnexion exponentielle, parsing JSON, heartbeat scheduling
- [ ] Vitest : `usePresence` rendu badge 0 / 1 / 3 / 5 utilisateurs
- [ ] Playwright E2E : ouvrir 2 onglets incognito sur `/billing/invoices/X/prepare` avec 2 users → badge visible dans les 2 onglets, disparition après close

## Risks & Open Questions

### Risques
- **Risque infra** : passage WSGI → ASGI en prod nécessite un redéploiement avec downtime court. Coordonner avec Philippe.
- **Risque perf** : si le channel layer Redis est saturé (plusieurs milliers de connexions simultanées), latence dégradée. À MVP-1, volume faible (≤ 100 users concurrents) — OK.
- **Risque sécurité** : JWT passé en query string peut être loggé → utiliser sous-protocole WebSocket ou premier message `auth` plutôt que query param.
- **Risque compat nginx Hostinger** : vérifier que la version nginx Docker supporte les directives `Upgrade` / `Connection` proprement.

### Questions ouvertes
- **Q1** : Le signal `post_save` pour push dashboard peut générer **trop** d'events (ex : import massif). Ajouter un mécanisme de **debounce** (ex : tâche Celery qui agrège et push toutes les 2s) ? → à décider avec Philippe, défaut : signal immédiat mais avec throttle côté consumer.
- **Q2** : Le badge presence doit-il **bloquer** l'édition (lecture seule si quelqu'un d'autre édite) ou **juste informer** ? Architecture.md laisse entendre informer uniquement (combiné à l'optimistic lock NFR31). Confirmer.
- **Q3** : Cleanup Redis si worker crash — compter sur TTL 60s ou ajouter job Celery de nettoyage ?

## Dev Agent Record
### Agent Model Used
_To be filled by dev agent_
### Completion Notes List
_To be filled during implementation_
### Change Log
- 2026-04-21: Story drafted from module-projets.md §9.5, confirmed MVP-1 scope by Philippe
### File List
_To be filled during implementation_

## References
- [_bmad-output/planning-artifacts/prd.md](../planning-artifacts/prd.md) NFR32
- [_bmad-output/planning-artifacts/architecture.md](../planning-artifacts/architecture.md) §Real-Time Presence L413-418, §129
- [_bmad-output/planning-artifacts/epics.md](../planning-artifacts/epics.md) L267, L277, L845, L1376, L1419
- [_bmad-output/planning-artifacts/module-projets.md](../planning-artifacts/module-projets.md) §9.5
- [.claude/rules/security.md](../../.claude/rules/security.md) — pas de JWT en query string, logs sans données sensibles
- [.claude/rules/deployment.md](../../.claude/rules/deployment.md) — à enrichir avec ASGI + WebSocket
- Story 12.3 (Finance données réelles) — consomme `useDashboardRealtime` sur Finance tab
- NFR31 — optimistic locking (complémentaire à presence indicator)
