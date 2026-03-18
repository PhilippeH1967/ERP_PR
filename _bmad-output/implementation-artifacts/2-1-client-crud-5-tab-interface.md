# Story 2.1: Client CRUD & 5-Tab Interface

Status: done

## Story

As a **Finance user**,
I want to create and manage clients via a 5-tab interface with inline editing,
So that all client information is centralized and structured.

## Acceptance Criteria

1. **Given** an authenticated Finance or Admin user **When** I click "Nouveau client" **Then** a creation form opens with fields: name, legal_entity, alias, sector
2. **And** The form calls POST /api/v1/clients/ and redirects to the detail page
3. **And** On the detail page, I can edit fields inline (click to edit, save on blur)
4. **And** The Contacts tab has an "Ajouter un contact" button with a form (name, role, email, phone, language)
5. **And** The Addresses tab has an "Ajouter une adresse" button with a form
6. **And** The Billing tab shows payment_terms_days and default_invoice_template as editable fields
7. **And** The CRM tab shows associe_en_charge and notes as editable fields
8. **And** Optimistic locking: If-Match header sent on PATCH, 409 shows conflict dialog
9. **And** The client list has pagination (25 per page)
10. **And** Route /clients/new is registered in the router

## Tasks / Subtasks

### Backend (DONE)
- [x] Client, Contact, ClientAddress models with TenantScopedModel + VersionedModel
- [x] ClientSerializer with OptimisticLockMixin, nested contacts/addresses
- [x] ClientViewSet with CRUD, search, filter, ordering, tenant isolation
- [x] ContactViewSet + ClientAddressViewSet nested under /clients/{id}/
- [x] financial_summary action with real billing services
- [x] 17 backend tests (8 models + 9 views)

### Frontend (TODO)
- [ ] Task F1: Client creation form (AC: #1, #2, #10)
  - [ ] F1.1 Create `features/clients/components/ClientCreateModal.vue` — SlideOver with form fields: name*, legal_entity, alias, sector, status
  - [ ] F1.2 Form validation with VeeValidate+Zod: name required, alias optional
  - [ ] F1.3 On submit: call `clientApi.create()`, on success redirect to `/clients/{id}`
  - [ ] F1.4 Register route `/clients/new` in router (or use modal from list)

- [ ] Task F2: Inline editing on ClientDetail tabs (AC: #3, #6, #7)
  - [ ] F2.1 Convert Identification tab from read-only `<p>` to editable `<input>` fields with save on blur
  - [ ] F2.2 Billing tab: editable payment_terms_days (number) + default_invoice_template (text)
  - [ ] F2.3 CRM tab: editable associe_en_charge (text) + notes (textarea)
  - [ ] F2.4 On blur: call `store.updateClient(id, { field: value })` with optimistic locking
  - [ ] F2.5 Show green feedback on successful save, red on error

- [ ] Task F3: Add/edit contacts in Contacts tab (AC: #4)
  - [ ] F3.1 "Ajouter un contact" button opens inline form at top of list
  - [ ] F3.2 Form fields: name*, role, email, phone, language_preference (fr/en select)
  - [ ] F3.3 On submit: call `clientApi.createContact(clientId, data)`, refresh list
  - [ ] F3.4 Each contact card has "Modifier" / "Supprimer" actions

- [ ] Task F4: Add/edit addresses in Addresses tab (AC: #5)
  - [ ] F4.1 "Ajouter une adresse" button opens inline form
  - [ ] F4.2 Form fields: address_line_1*, address_line_2, city*, province, postal_code*, country, is_billing, is_primary
  - [ ] F4.3 On submit: call `clientApi.createAddress(clientId, data)`, refresh list

- [ ] Task F5: Pagination on client list (AC: #9)
  - [ ] F5.1 Add page/page_size query params to `clientApi.list()`
  - [ ] F5.2 Display pagination controls (prev/next + page indicator) below table
  - [ ] F5.3 Update store to track pagination meta (count, next, previous)

- [ ] Task F6: Optimistic locking conflict handling (AC: #8)
  - [ ] F6.1 On 409 from updateClient: show BaseModal with "Conflit de version" message
  - [ ] F6.2 Options: "Recharger" (refetch) or "Forcer" (retry without If-Match)

- [ ] Task F7: Tests (AC: #1-#10)
  - [ ] F7.1 Test useClientStore: createClient, updateClient with version
  - [ ] F7.2 Test that client creation API is called correctly
  - [ ] F7.3 ESLint 0 errors

## Dev Notes

### Files to CREATE
| File | Purpose |
|------|---------|
| `features/clients/components/ClientCreateModal.vue` | Slide-over creation form |
| `features/clients/components/EditableField.vue` | Reusable inline-edit field (click→input→blur save) |
| `features/clients/components/ContactForm.vue` | Inline contact add/edit form |
| `features/clients/components/AddressForm.vue` | Inline address add/edit form |

### Files to MODIFY
| File | Change |
|------|--------|
| `features/clients/views/ClientList.vue` | Add pagination controls |
| `features/clients/views/ClientDetail.vue` | Convert to inline-edit mode |
| `features/clients/stores/useClientStore.ts` | Add pagination, deleteClient |
| `features/clients/api/clientApi.ts` | Add pagination params |
| `src/router/index.ts` | Add /clients/new route (or modal trigger) |

### Existing Backend API Available
```
GET    /api/v1/clients/                    — List (paginated, search, filter)
POST   /api/v1/clients/                    — Create
GET    /api/v1/clients/{id}/               — Retrieve with nested contacts/addresses
PATCH  /api/v1/clients/{id}/               — Update with If-Match version
DELETE /api/v1/clients/{id}/               — Delete

GET    /api/v1/clients/{id}/contacts/      — List contacts
POST   /api/v1/clients/{id}/contacts/      — Add contact
PATCH  /api/v1/clients/{id}/contacts/{cid}/ — Edit contact
DELETE /api/v1/clients/{id}/contacts/{cid}/ — Delete contact

GET    /api/v1/clients/{id}/addresses/     — List addresses
POST   /api/v1/clients/{id}/addresses/     — Add address
```

### EditableField Pattern
```vue
<!-- Reusable: click to edit, blur to save -->
<EditableField
  :value="store.currentClient.name"
  label="Nom légal"
  @save="(val) => store.updateClient(id, { name: val })"
/>
```

### References
- [Source: epics.md — Story 2.1 AC: 5-tab interface, CRUD]
- [Source: audit — Backend 90% done, frontend needs forms]
- [Source: ux-design-specification.md — Form patterns, SlideOver for creation]

## Dev Agent Record

### Agent Model Used
(to be filled by dev agent)

### Debug Log References

### Completion Notes List
- Backend fully implemented (models, serializers, views, 17 tests)
- Frontend has ClientList + ClientDetail read-only
- Story file created for BMAD frontend completion

### Change Log
- 2026-03-18: Backend implemented as part of Epic 2 batch
- 2026-03-18: Story file created after audit — frontend tasks defined

### File List

**Backend (done):**
- backend/apps/clients/models.py
- backend/apps/clients/serializers.py
- backend/apps/clients/views.py
- backend/apps/clients/urls.py
- backend/apps/clients/services.py
- backend/apps/clients/tests/test_models.py
- backend/apps/clients/tests/test_views.py

**Frontend (in progress):**
- frontend/src/features/clients/types/client.types.ts
- frontend/src/features/clients/api/clientApi.ts
- frontend/src/features/clients/stores/useClientStore.ts
- frontend/src/features/clients/views/ClientList.vue
- frontend/src/features/clients/views/ClientDetail.vue
