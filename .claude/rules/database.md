# database.md

Règles à lire **avant toute modification** touchant :
- `backend/**/models.py`
- `backend/**/migrations/**`
- Requêtes ORM complexes (filtrage, aggregations)

## Migrations

### Atomicité
- **Une migration = un changement cohérent** (ajout d'un modèle, d'un champ, modification d'une contrainte)
- Ne pas mélanger plusieurs fonctionnalités dans une seule migration
- Nommer les migrations avec un suffixe explicite : `0042_add_invoice_status_field.py`

### Destructivité
- **Pas de `DROP` destructif** sans validation explicite de l'utilisateur
- `RemoveField`, `DeleteModel` : confirmer avec l'utilisateur avant
- `AlterField` qui réduit la taille d'un `CharField` : risque de troncation, valider
- Préférer : déprécier → migrer les données → supprimer dans une migration ultérieure

### Backfill de données
- Pour les migrations qui modifient la sémantique d'un champ : **RunPython** avec une fonction `reverse` symétrique
- Tester le backfill sur une copie de la DB prod avant merge

### Validation
```bash
cd backend && python manage.py makemigrations --dry-run     # avant tout
cd backend && python manage.py makemigrations --check       # CI
cd backend && python manage.py migrate --plan               # inspection
```

## Modèles Django

### Champs
- **Type hints** sur `Meta`, méthodes personnalisées, managers
- `verbose_name` en français pour les admins
- `help_text` pour les champs non triviaux
- `blank=True, null=True` : jamais automatique — réfléchir à la sémantique

### Contraintes
- `unique_together` / `UniqueConstraint` pour les contraintes métier
- `CheckConstraint` pour les invariants (ex : `date_fin >= date_debut`)
- `db_index=True` sur les colonnes filtrées/triées fréquemment

### Managers
- Pas de logique métier dans `models.py` — utiliser un manager custom ou un service
- `objects = CustomManager()` pour encapsuler les querysets fréquents

## Performance

### N+1
- **Toujours** `select_related` pour les FK accédées dans une liste
- **Toujours** `prefetch_related` pour les M2M / reverse FK
- Vérifier avec `assertNumQueries` dans les tests DRF

### Pagination
- **Obligatoire** sur toutes les listes (`PageNumberPagination` ou `CursorPagination`)
- Ne jamais retourner un queryset brut sur un endpoint public

### Index
- Index sur les colonnes filtrées (WHERE)
- Index composites pour les tris multi-colonnes
- Vérifier les plans d'exécution sur les requêtes lentes (`EXPLAIN ANALYZE`)

## Intégrité et transactions

- `@transaction.atomic` sur les opérations multi-modèles (ex : création projet + phases + tâches)
- `select_for_update()` pour éviter les races sur les compteurs / séquences

## Tests

- Fixtures via `factory_boy`, jamais de SQL brut
- Tester les contraintes d'intégrité (`IntegrityError` sur doublons, FK invalides)
- Tester `assertNumQueries` sur les endpoints à fort volume

## Cas à remonter immédiatement à l'utilisateur

- Migration `RemoveField` / `DeleteModel` non justifiée dans la tâche
- Requête N+1 sur un endpoint public
- `raw()` SQL inattendu
- Pagination manquante sur une liste
