# Story 11.3: Parallel Run Period

Status: done

## Story

As a **system administrator**,
I want to export data in multiple formats (CSV, Excel, PDF) for comparison with ChangePoint,
So that I can run both systems in parallel and validate data consistency before cutover.

## Acceptance Criteria

- ExportJob model tracks bulk export operations
- Fields: export_type, format (CSV/Excel/PDF), status lifecycle, file_url, record_count
- Status choices mirror ImportJob (pending/processing/completed/failed)
- Jobs are tenant-scoped and track created_by user
- file_url stores the path to the generated export file

## Tasks / Subtasks

- [x] Task 1: Implement ExportJob model
  - [x] 1.1 Created ExportJob model extending TenantScopedModel
  - [x] 1.2 Fields: export_type (CharField), format (choices: csv/excel/pdf), status (4-choice lifecycle), created_by (FK), file_url (CharField 500), record_count
  - [x] 1.3 db_table set to `data_ops_export_job`
  - [x] 1.4 Included in 0001_initial migration

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- ExportJob model: export_type, format (csv/excel/pdf choices), status (4-choice lifecycle), created_by (user FK, SET_NULL), file_url (CharField, blank default), record_count
- Format choices: CSV, Excel, PDF — covers parallel run comparison needs and Intacct integration
- Same status lifecycle as ImportJob for consistency
- db_table: `data_ops_export_job`, ordered by `-created_at`

### Change Log
- 2026-03-18: Implemented as part of Epic 11 batch

### File List
- backend/apps/data_ops/models.py (ExportJob)
- backend/apps/data_ops/migrations/0001_initial.py
