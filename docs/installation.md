# Installation & Démarrage

## Prérequis

- Docker Desktop
- Git

## Démarrage rapide

```bash
# Cloner le repo
git clone https://github.com/PhilippeH1967/ERP_PR.git
cd ERP_PR

# Copier la configuration
cp .env.example .env

# Lancer les conteneurs
docker compose up -d

# Vérifier les services
docker compose ps
# → django (8000), vue (5174), postgres (5436), redis (6379)

# Appliquer les migrations
docker compose exec django python manage.py migrate

# Créer le tenant initial
docker compose exec django python manage.py seed_reference_data

# Seeder les données de base
docker compose exec django python manage.py seed_templates
docker compose exec django python manage.py seed_expense_categories

# Accéder à l'application
open http://localhost:5174
```

## Comptes de test

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| admin@provencher-roy.com | Test1234! | ADMIN |
| pm@test.com | Test1234! | PM |
| pm2@test.com | Test1234! | PM |
| finance@test.com | Test1234! | FINANCE |
| paie@test.com | Test1234! | PAIE |
| employe@test.com | Test1234! | EMPLOYEE |

## Services Docker

| Service | Port | URL |
|---------|------|-----|
| django | 8000 | http://localhost:8000/api/v1/ |
| vue | 5174 | http://localhost:5174 |
| postgres | 5436 | postgres://localhost:5436/erp |
| redis | 6379 | redis://localhost:6379 |

## Commandes utiles

```bash
# Tests backend
docker compose exec django python -m pytest

# Migrations
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate

# Shell Django
docker compose exec django python manage.py shell

# Logs
docker compose logs django -f
docker compose logs vue -f

# Rebuild
docker compose up -d --build
```
