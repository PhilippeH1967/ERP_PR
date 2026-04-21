# deployment.md

Règles et commandes de déploiement. À lire **avant toute modification** touchant :
- `docker-compose*.yml`
- `backend/config/settings/prod.py`
- `nginx/` ou tout fichier de reverse proxy
- `.env.production` (référence uniquement — jamais committé)

## Serveur de test / démo (Hostinger)

- **URL** : https://srv1248490.hstgr.cloud
- **SSH** : `root@srv1248490.hstgr.cloud` — accès via terminal web hPanel (SCP bloqué depuis réseau local)
- **Repo sur serveur** : `/opt/erp`
- **Env prod** : `/opt/erp/.env.production`

## Architecture Docker prod

- **nginx** (ports 80 + 443) — reverse proxy, HTTPS Let's Encrypt
- **django** (gunicorn, port 8000 interne)
- **vue** (nginx SPA, port 80 interne)
- **postgres:16.6-alpine**
- **redis:7.2-alpine**
- **celery_worker** + **celery_beat**

## Commandes de déploiement

**Important : une commande par ligne, pas de multi-lignes.**

```bash
cd /opt/erp && git pull origin main
docker compose -f docker-compose.prod.yml --env-file .env.production up -d --build django vue
docker compose -f docker-compose.prod.yml --env-file .env.production exec django python manage.py migrate
```

## Exécuter un script Python dans le container

```bash
docker compose -f docker-compose.prod.yml --env-file .env.production exec django mkdir -p /app/scripts
docker cp /opt/erp/backend/scripts/SCRIPT.py erp-django-1:/app/scripts/SCRIPT.py
docker compose -f docker-compose.prod.yml --env-file .env.production exec -T django python manage.py shell < /opt/erp/backend/scripts/SCRIPT.py
```

**Note** : les scripts standalone avec `django.setup()` ne fonctionnent pas (module `config` introuvable). Utiliser `manage.py shell < script.py`.

## Comptes de test (Hostinger uniquement)

- `admin@provencher-roy.com` / `Test1234!` (ADMIN)
- `pm@test.com` / `Test1234!` (PM)
- `finance@test.com` / `Test1234!` (FINANCE)
- `paie@test.com` / `Test1234!` (PAIE)
- `employe@test.com` / `Test1234!` (EMPLOYEE)
- 24 comptes ChangePoint importés (`amonty`, `jbelanger`, etc.) / `Test1234!`

**Ne jamais** utiliser ces credentials en dehors du serveur de démo.

## Pré-déploiement — checklist

- [ ] Tests backend passent (`pytest`)
- [ ] Tests frontend passent (`npm run test:unit` + `test:e2e`)
- [ ] Migrations vérifiées (`makemigrations --check`)
- [ ] Pas de secret committé (vérifier `git diff`)
- [ ] `DEBUG = False` en prod settings
- [ ] `ALLOWED_HOSTS` inclut le domaine prod
- [ ] Changelog / message de commit clair

## Cas à remonter immédiatement à l'utilisateur

- Échec de migration en prod
- Container qui redémarre en boucle
- Certificat Let's Encrypt expiré
- Fuite de secret détectée dans un commit
