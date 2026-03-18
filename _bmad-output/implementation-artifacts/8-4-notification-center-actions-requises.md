# Story 8.4: Notification Center & Actions Requises

Status: done

## Story

As a **user**,
I want a notification center with configurable preferences,
So that I receive relevant alerts for pending actions and can control which notifications I get.

## Acceptance Criteria

- Notification model stores user, notification_type, message, read_at
- NotificationPreference model stores email_enabled, subscribed_categories per user
- Both models are tenant-scoped via TenantScopedModel
- Notification ordering is by most recent first (-created_at)
- NotificationPreference is one-to-one per user

## Tasks / Subtasks

- [x] Task 1: Create notifications Django app with models
  - [x] 1.1 Created `backend/apps/notifications/` app scaffold
  - [x] 1.2 Implemented Notification model (user FK, notification_type CharField, message TextField, read_at nullable DateTimeField)
  - [x] 1.3 Implemented NotificationPreference model (user OneToOneField, email_enabled BooleanField, subscribed_categories JSONField)
  - [x] 1.4 Created initial migration (0001_initial.py)

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- Notification model extends TenantScopedModel with user FK, notification_type, message, read_at
- NotificationPreference model extends TenantScopedModel with user OneToOneField, email_enabled (default True), subscribed_categories (JSONField, default list)
- Custom db_table names: `notifications_notification`, `notifications_preference`
- Notification ordered by `-created_at`; preference has unique user constraint via OneToOneField

### Change Log
- 2026-03-18: Implemented as part of Epic 8 batch

### File List
- backend/apps/notifications/__init__.py
- backend/apps/notifications/apps.py
- backend/apps/notifications/models.py
- backend/apps/notifications/tests/__init__.py
- backend/apps/notifications/migrations/__init__.py
- backend/apps/notifications/migrations/0001_initial.py
