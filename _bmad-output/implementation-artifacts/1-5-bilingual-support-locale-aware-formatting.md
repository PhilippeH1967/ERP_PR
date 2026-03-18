# Story 1.5: Bilingual Support & Locale-Aware Formatting

Status: done

## Story

As an **employee**,
I want to use the application in French or English with properly formatted dates and numbers,
So that I can work in my preferred language.

## Acceptance Criteria

1. **Given** an authenticated user with language preference "fr" **When** I navigate any screen **Then** all UI labels, buttons, and messages display in French
2. **And** I can switch language via user preferences and the change takes effect immediately
3. **And** All dates render as YYYY-MM-DD (Quebec standard) with locale-aware formatters
4. **And** All currency amounts render with proper separators ($10,200.50 for EN, 10 200,50 $ for FR)
5. **And** All monetary amounts in API responses are `string` type (not float)
6. **And** Vue I18n is configured with externalized translation files (no hardcoded text — FR76b)
7. **And** The frontend uses system font stack with monospace for financial amounts

## Tasks / Subtasks

- [ ] Task 1: Expand Vue I18n with locale switching (AC: #1, #2, #6)
- [ ] Task 2: Create locale-aware formatting utilities (AC: #3, #4)
- [ ] Task 3: Create useLocale composable (AC: #2)
- [ ] Task 4: Verify font stack and monospace (AC: #7)
- [ ] Task 5: Backend — monetary string serialization (AC: #5)
- [ ] Task 6: Tests

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)
### Debug Log References
### Completion Notes List
### Change Log
### File List
