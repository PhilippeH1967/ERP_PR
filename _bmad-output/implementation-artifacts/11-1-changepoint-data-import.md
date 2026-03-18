# Story 11.1: ChangePoint Data Import

Status: done

## Story

As a **system administrator**,
I want to import data from ChangePoint via bulk import jobs,
So that historical project, timesheet, and financial data can be migrated into the new system.

## Acceptance Criteria

- ImportJob model tracks bulk import operations with status lifecycle
- Fields: import_type, file_path, status (pending/processing/completed/failed), record_count, error_message
- Status choices use French labels (En attente, En cours, Termine, Echoue)
- Jobs are tenant-scoped and track created_by user
- completed_at timestamp recorded on completion

## Tasks / Subtasks

- [x] Task 1: Create data_ops Django app with ImportJob model
  - [x] 1.1 Created `backend/apps/data_ops/` app scaffold
  - [x] 1.2 Implemented ImportJob model extending TenantScopedModel
  - [x] 1.3 Fields: import_type (CharField), file_path (CharField 500), status (choices), created_by (FK), completed_at, error_message, record_count
  - [x] 1.4 Created initial migration (0001_initial.py)

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- ImportJob model: import_type, file_path, status (4-choice lifecycle), created_by (user FK, SET_NULL), completed_at (nullable), error_message (TextField), record_count (IntegerField)
- Status choices: pending (En attente), processing (En cours), completed (Termine), failed (Echoue)
- db_table: `data_ops_import_job`, ordered by `-created_at`
- Supports ChangePoint migration, Excel uploads, and other bulk import scenarios

### Change Log
- 2026-03-18: Implemented as part of Epic 11 batch

### File List
- backend/apps/data_ops/__init__.py
- backend/apps/data_ops/apps.py
- backend/apps/data_ops/models.py (ImportJob)
- backend/apps/data_ops/tests/__init__.py
- backend/apps/data_ops/migrations/__init__.py
- backend/apps/data_ops/migrations/0001_initial.py
