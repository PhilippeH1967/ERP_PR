# Story 1.6: Frontend Shell & Design System Foundation

Status: done

## Story

As a **user**,
I want a consistent application shell with sidebar navigation, top bar, and role-based landing page,
So that I can navigate the application efficiently.

## Acceptance Criteria

1. **Given** an authenticated user **When** I log in **Then** I see MainLayout with collapsible sidebar, top bar (search, notifications bell, user menu)
2. **And** The sidebar shows navigation items filtered by my role permissions
3. **And** I land on my role-adaptive default page (Employee → /timesheets, PM → /dashboard, Finance → /billing)
4. **And** TailwindCSS 4 design tokens are configured (colors, typography, spacing per UX spec)
5. **And** Headless UI components (Modal, SlideOver, Tabs, Combobox) are available in shared/components/
6. **And** Dark mode toggle works via Tailwind `dark:` prefix
7. **And** The DRF API returns standardized responses (already done in Story 1.1)
8. **And** Axios interceptor handles 401/403/409/500 (already done in Story 1.3)

## Tasks / Subtasks

- [x] Task 1: MainLayout with sidebar + topbar
- [x] Task 2: Headless UI components (BaseModal, SlideOver, ToastNotification)
- [x] Task 3: Design tokens with dark mode + role colors
- [x] Task 4: Route structure with MainLayout wrapper + child routes
- [x] Task 5: i18n navigation keys (FR/EN)
- [x] Task 6: All tests pass, eslint 0 errors

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- MainLayout: collapsible sidebar (w-60/w-16), topbar (h-14) with search, locale toggle, notifications, user menu
- BaseModal.vue: Headless UI Dialog with transitions
- SlideOver.vue: Headless UI slide-from-right panel
- ToastNotification.vue: auto-dismiss with type variants (success/error/warning/info)
- Design tokens: role colors (employee blue, PM amber, finance green, director purple, admin gray)
- Dark mode: @media prefers-color-scheme with CSS variable overrides
- Router: MainLayout wraps all authenticated routes, child routes for dashboard/timesheets/projects/billing/expenses
- 62 backend + 11 frontend tests, ruff + eslint clean

### Change Log
- 2026-03-17: Story 1.6 implemented — frontend shell, design system, Headless UI components

### File List

**Modified:**
- frontend/src/router/index.ts — MainLayout wrapper, child routes
- frontend/src/locales/fr.json — added nav.* keys
- frontend/src/locales/en.json — added nav.* keys
- frontend/src/assets/styles/main.css — dark mode, role colors, system font stack

**Created:**
- frontend/src/shared/layouts/MainLayout.vue — application shell
- frontend/src/shared/components/BaseModal.vue — Headless UI modal
- frontend/src/shared/components/SlideOver.vue — Headless UI slide-over
- frontend/src/shared/components/ToastNotification.vue — auto-dismiss toast
