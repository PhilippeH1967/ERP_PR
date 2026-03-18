# Story 2.3: Client Financial History & Project Linking

Status: done

## Story

As a **Finance user**,
I want to see per-client financial history and linked projects,
So that I can assess client health and relationship value.

## Acceptance Criteria

1. **Given** a client with projects **When** I view the detail page **Then** I see total CA, outstanding invoices, payment history
2. **And** An aging analysis shows outstanding invoices grouped by 0-30j, 31-60j, 61-90j, 90+j
3. **And** A projects list shows linked projects with code, name, status

## Tasks / Subtasks

### Backend (DONE)
- [x] GET /api/v1/clients/{id}/financial_summary/ with real aggregation
- [x] Aging analysis integrated from billing services

### Frontend
- [ ] F1: Add "Financier" tab to ClientDetail with financial summary cards
- [ ] F2: Add aging analysis bar chart
- [ ] F3: Add linked projects list (fetch from /api/v1/projects/?client={id})

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### File List
