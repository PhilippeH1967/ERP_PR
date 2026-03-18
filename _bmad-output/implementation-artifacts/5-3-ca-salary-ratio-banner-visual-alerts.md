# Story 5.3: CA/Salary Ratio Banner and Visual Alerts

Status: done

## Story
As a project manager, I want to see the CA/Salary ratio prominently displayed during billing, so that I can identify projects where revenue does not cover salary costs.

## Acceptance Criteria
- calculate_ca_salary_ratio service function returns invoiced, salary_cost, ratio_percent, hours_consumed
- Computes ratio as (invoiced / salary_cost * 100)
- Uses TimeEntry hours with placeholder average rate (will use RateGrid when available)
- Returns Decimal-precision results as strings

## Tasks / Subtasks
- [x] Create calculate_ca_salary_ratio service function
- [x] Aggregate Invoice total_amount for the project
- [x] Aggregate TimeEntry hours for the project
- [x] Calculate ratio with placeholder avg_rate ($85.00)
- [x] Return dict with invoiced, salary_cost, ratio_percent, hours_consumed
- [x] Write tests for ratio calculation

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- calculate_ca_salary_ratio in services.py aggregates invoices and time entries
- Placeholder rate of $85.00/hr used until RateGrid integration
- Returns ratio as percentage with 2-decimal precision
- Handles zero salary_cost edge case (returns 0)
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/services.py
- backend/apps/billing/tests/test_services.py
