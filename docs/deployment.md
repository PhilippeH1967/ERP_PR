# Déploiement

## Environnement Docker

Le projet utilise Docker Compose avec les services suivants :

| Service | Image | Port | Rôle |
|---------|-------|------|------|
| django | Custom (Dockerfile) | 8000 | API backend (uvicorn ASGI) |
| vue | Custom (Dockerfile) | 5174 | Frontend dev server (Vite) |
| postgres | postgres:16.6-alpine | 5436 | Base de données |
| redis | redis:7.2-alpine | 6379 | Cache + Celery broker |
| celery_worker | Même image django | — | Tâches async |
| celery_beat | Même image django | — | Scheduler (relances, expirations) |

## Variables d'environnement

Voir `.env.example` pour la liste complète. Variables critiques :

```
DATABASE_URL=postgres://erp:erp@postgres:5432/erp
REDIS_URL=redis://redis:6379/0
SECRET_KEY=...
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.local
```

## Celery Beat Schedule

| Tâche | Fréquence | Fonction |
|-------|-----------|----------|
| Relance timesheets (mercredi) | Wed 17h | send_timesheet_reminders |
| Relance timesheets (vendredi) | Fri 12h | send_timesheet_reminders |
| Escalade PM (vendredi) | Fri 17h | escalate_missing_timesheets |
| Expiration délégations | Daily 1h | expire_delegations |

## Mise à jour

```bash
git pull origin main
docker compose up -d --build
docker compose exec django python manage.py migrate
docker compose exec django python manage.py collectstatic --noinput
```

## Sauvegarde

```bash
# Backup PostgreSQL
docker compose exec postgres pg_dump -U erp erp > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20260407.sql | docker compose exec -T postgres psql -U erp erp
```
