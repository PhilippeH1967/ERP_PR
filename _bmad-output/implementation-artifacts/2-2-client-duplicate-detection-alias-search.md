# Story 2.2: Client Duplicate Detection & Alias Search

Status: done

## Story

As a **Finance user**,
I want the system to detect potential duplicate clients on creation and search clients by alias,
So that the client registry stays clean and findable.

## Acceptance Criteria

1. **Given** I am creating a new client with name "Ville de Montréal" **When** a client "Ville de Montreal" already exists **Then** the system shows a warning with potential duplicates
2. **And** I can choose to "Voir l'existant", "Créer quand même", or cancel
3. **And** Duplicate detection uses name similarity and alias matching (FR86b)
4. **And** Each client has a unique alias searchable across the application (FR86c)
5. **And** The API exposes POST /api/v1/clients/check_duplicate/ endpoint

## Tasks / Subtasks

### Backend
- [x] detect_duplicate_client() service exists (name + alias matching)
- [ ] B1: Create /api/v1/clients/check_duplicate/ endpoint calling the service
- [ ] B2: Write test for duplicate detection service
- [ ] B3: Write test for check_duplicate endpoint

### Frontend
- [ ] F1: Create DuplicateDetectionModal.vue showing matches
- [ ] F2: Integrate modal in ClientCreateModal — check on name blur before submit
- [ ] F3: Options: "Voir l'existant" (navigate), "Créer quand même" (proceed), "Annuler"

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### File List
