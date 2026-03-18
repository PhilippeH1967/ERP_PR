# Story 9.3: Department Assistant Delegation

Status: done

## Story

As a **department director**,
I want to assign a department assistant role to a team member,
So that they can perform administrative tasks on my behalf for projects within the department.

## Acceptance Criteria

- DEPT_ASSISTANT role exists in the Role enum
- DEPT_ASSISTANT is available for per-project assignment via ProjectRole
- Role label is bilingual: "Adjoint(e) de departement"
- Role can be assigned like any other role in the RBAC framework

## Tasks / Subtasks

- [x] Task 1: Add DEPT_ASSISTANT to Role enum
  - [x] 1.1 Added `DEPT_ASSISTANT = "DEPT_ASSISTANT", "Adjoint(e) de departement"` to Role TextChoices (Story 1.4)
  - [x] 1.2 Role is selectable in ProjectRole assignments
  - [x] 1.3 Permission framework recognizes DEPT_ASSISTANT for access checks

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- DEPT_ASSISTANT added as 6th role in the 8-role Role enum (TextChoices)
- Full Role enum: EMPLOYEE, PM, PROJECT_DIRECTOR, BU_DIRECTOR, FINANCE, DEPT_ASSISTANT, PROPOSAL_MANAGER, ADMIN
- ProjectRole model allows assigning DEPT_ASSISTANT to any user for any project
- Permission checks in core/permissions.py recognize DEPT_ASSISTANT role

### Change Log
- 2026-03-18: Implemented as part of Epic 9 batch

### File List
- backend/apps/core/models.py (Role.DEPT_ASSISTANT, ProjectRole)
