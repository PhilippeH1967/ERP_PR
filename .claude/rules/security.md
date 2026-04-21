# security.md

Règles de sécurité à lire **avant toute modification** touchant :
- authentification / permissions
- endpoints DRF (ViewSets, APIView)
- serializers manipulant des données sensibles ou personnelles
- fichiers `.env*`, settings, ou code de déploiement

## Secrets et credentials

- **Jamais** de `SECRET_KEY`, token, mot de passe, clé API dans le code ou les tests
- Toujours passer par `os.environ` / `django-environ` via `.env` (hors Git)
- `.env.production` : **jamais** committé
- Avant tout commit, vérifier qu'aucune valeur sensible n'a fuité

## Données personnelles (protection obligatoire)

**Toute donnée personnelle doit être protégée.** Concerne : employés, clients, fournisseurs, contacts, utilisateurs.

### Données personnelles identifiées
- Nom, prénom, adresse personnelle, téléphone, email personnel
- Date de naissance, numéro d'assurance sociale (NAS), numéro d'employé
- Salaire, taux horaire, fiches de paie, comptes bancaires
- Données médicales liées aux congés (arrêts maladie, handicap)
- Identifiants de connexion, tokens de session

### Règles techniques
- **Chiffrement en transit** : HTTPS obligatoire (Let's Encrypt en prod, pas de HTTP même interne)
- **Chiffrement au repos** pour les champs sensibles (NAS, coordonnées bancaires) — utiliser `django-cryptography` ou équivalent
- **Jamais** de données personnelles dans :
  - Les logs applicatifs (mots de passe, tokens, NAS, salaires)
  - Les messages d'erreur renvoyés au frontend
  - Les exports CSV/PDF sans filtrage par permissions
  - Les URLs (utiliser POST body, pas querystring)
- **Minimisation** : ne jamais stocker ou afficher plus de données que nécessaire au cas d'usage
- **Rétention** : supprimer les données obsolètes selon la politique de conservation (à définir projet)

### Règles d'accès
- **Isolement** : un employé ne voit que ses propres fiches de paie, congés, évaluations
- **Principe du moindre privilège** : RH voit les fiches paie, PM voit uniquement les taux projet (pas le salaire brut)
- **Audit trail** : journaliser les accès/modifications sur les données sensibles (admin, paie, finance)
- **Export conforme** (RGPD / Loi 25 Québec) : les exports de données personnelles doivent être filtrés par propriétaire et journalisés

### Anonymisation en dev/test
- Jamais de données personnelles réelles en environnement de dev/test
- Utiliser `factory_boy` avec Faker pour générer des données synthétiques
- Si un dump prod est utilisé : anonymiser avant (scripts dédiés)

## Permissions DRF

- **Permissions restrictives par défaut** : `IsAuthenticated` au minimum, jamais `AllowAny` sans justification explicite
- **Permissions explicites** sur chaque ViewSet / APIView — pas d'héritage silencieux
- **Isolement des données** : un utilisateur ne doit voir/modifier que ses propres données, sauf rôle admin/PM explicite
- **Double-check admin** : `IsAdmin` côté backend **ET** route guard côté frontend
- **Tests obligatoires** : non-authentifié (401), authentifié lambda (403 ou filtre), admin (200) — voir [backend/CLAUDE.md](../../backend/CLAUDE.md)

## Protection CSRF et CORS

- **CSRF activé** sur toutes les vues qui modifient l'état (POST, PUT, PATCH, DELETE)
- Les endpoints DRF utilisent `SessionAuthentication` → CSRF vérifié automatiquement
- **CORS** : whitelist stricte des origines (`CORS_ALLOWED_ORIGINS`), jamais `CORS_ALLOW_ALL_ORIGINS=True` en prod

## Validation d'input

- **Toujours** dans le serializer (`validate_<field>`, `validate()`) — jamais dans la view
- Types stricts (`IntegerField`, `DateField`, `ChoiceField` avec `choices`)
- `max_length`, `min_value`, `max_value` explicites
- Pour les ForeignKey : `PrimaryKeyRelatedField` avec queryset filtré par permissions

## Protection injection

- **Usage exclusif de l'ORM Django** — pas de `raw()`, `RawSQL`, `extra()` sans revue
- Si `raw()` indispensable : paramètres bindés obligatoires (`%s`), jamais de f-string
- Requêtes `__icontains`, `__in` : via ORM, pas concaténation

## Logs et données sensibles

- **Jamais** logger mots de passe, tokens, numéros de carte, données personnelles sensibles
- `DEBUG = False` en prod (vérifié dans `config/settings/prod.py`)
- Les pages d'erreur 500 ne doivent **jamais** exposer la stack trace en prod

## Outils automatiques

- `ruff` avec `bandit` (règles `S`) détecte les vulnérabilités courantes
- Avant merge sur une PR sensible : lancer `/security-review` (skill Claude)

## Cas à remonter immédiatement à l'utilisateur

- Découverte d'un endpoint avec `AllowAny`
- Secret/token hardcodé dans le code ou dans un commit
- Faille de permission (utilisateur A peut voir les données de B)
- Stack trace exposée en prod
- Données personnelles exposées dans logs, URLs, ou exports non filtrés
- Absence de chiffrement sur un champ sensible (NAS, coordonnées bancaires)
