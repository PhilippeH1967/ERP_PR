import { test, expect, type Page } from '@playwright/test'

/**
 * E2E flow profils virtuels — onglet Équipe d'un projet.
 *
 * Ce test mocke toutes les API via route interception pour vérifier le
 * contrat d'affichage UI sans dépendre d'un backend réel :
 *   - état vide (aucun profil virtuel)
 *   - présence d'un profil virtuel actif + bouton Remplacer…
 *   - après remplacement, apparition dans "Historique des remplacements"
 *     avec le nom de l'employé remplaçant.
 */

type VR = {
  id: number
  project: number
  project_code: string
  name: string
  default_hourly_rate: string
  is_active: boolean
  replaced_by: number | null
  replaced_by_name: string
  replaced_at: string | null
  notes: string
  created_at: string
}

const PROJECT = {
  id: 1,
  code: 'P-001',
  name: 'Projet démo',
  status: 'ACTIVE',
  client: null,
  client_name: '',
  business_unit: null,
  is_internal: false,
  is_public: true,
  is_consortium: false,
  consortium: null,
  consortium_name: '',
  services_transversaux: false,
  legal_entity: null,
  start_date: '2026-01-01',
  end_date: '2026-12-31',
  pm: 1,
  associate_in_charge: 1,
  invoice_approver: null,
  bu_director: null,
  phases: [],
  support_services: [],
  version: 1,
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
}

const USER = {
  id: 1,
  username: 'alice',
  email: 'alice@test.com',
  first_name: 'Alice',
  last_name: 'Martin',
  tenant_id: 1,
  roles: ['PROJECT_DIRECTOR'],
}

async function routeAuth(page: Page) {
  // Catch-all fallback : tout endpoint non explicitement mocké renvoie {} 200
  // (évite 404/500 → interceptor axios → redirect login)
  await page.route('**/api/v1/**', (r) => r.fulfill({ json: { results: [] } }))
  await page.route('**/api/v1/auth/config/', (r) =>
    r.fulfill({ json: { sso_available: false, sso_only: false } }),
  )
  await page.route('**/api/v1/auth/token/', (r) =>
    r.fulfill({ json: { access: 'fake', refresh: 'fake' } }),
  )
  await page.route('**/api/v1/auth/me/', (r) => r.fulfill({ json: USER }))
  await page.route('**/api/v1/users/search/**', (r) =>
    r.fulfill({ json: { results: [{ id: 42, username: 'bob', email: 'bob@x.com' }] } }),
  )
}

async function routeProject(page: Page) {
  await page.route(`**/api/v1/projects/1/`, (r) => r.fulfill({ json: PROJECT }))
  await page.route('**/api/v1/projects/1/team_stats/', (r) =>
    r.fulfill({ json: { budget_status: 'green', over_budget_phases: 0, total_phases: 0 } }),
  )
  await page.route('**/api/v1/projects/1/budget-summary/', (r) =>
    r.fulfill({ json: {} }),
  )
  await page.route('**/api/v1/allocations/**', (r) =>
    r.fulfill({ json: { results: [] } }),
  )
  await page.route('**/api/v1/amendments/**', (r) =>
    r.fulfill({ json: { results: [] } }),
  )
  await page.route('**/api/v1/time-entries/**', (r) =>
    r.fulfill({ json: { results: [] } }),
  )
}

test.describe('Onglet Équipe — profils virtuels', () => {
  test.beforeEach(async ({ page }) => {
    await routeAuth(page)
    await routeProject(page)
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake')
      localStorage.setItem('refresh_token', 'fake')
    })
  })

  test('affiche l\'état vide quand aucun profil virtuel', async ({ page }) => {
    await page.route('**/api/v1/virtual-resources/**', (r) =>
      r.fulfill({ json: { results: [] } }),
    )
    await page.goto('/projects/1?tab=execution/team')
    await expect(page.locator('[data-virtuals-empty]')).toBeVisible({ timeout: 10_000 })
    await expect(page.locator('[data-virtuals-empty]')).toContainText('Aucun profil virtuel')
  })

  test('affiche un profil virtuel actif avec le bouton Remplacer', async ({ page }) => {
    const active: VR = {
      id: 10, project: 1, project_code: 'P-001',
      name: 'Architecte senior', default_hourly_rate: '95.00',
      is_active: true, replaced_by: null, replaced_by_name: '', replaced_at: null,
      notes: '', created_at: '2026-01-01T00:00:00Z',
    }
    await page.route('**/api/v1/virtual-resources/**', (r) =>
      r.fulfill({ json: { results: [active] } }),
    )
    await page.goto('/projects/1?tab=execution/team')
    await expect(page.locator('[data-virtual-row]')).toHaveCount(1, { timeout: 10_000 })
    await expect(page.locator('[data-virtual-row]')).toContainText('Architecte senior')
    await expect(page.locator('[data-replace-start]')).toBeVisible()
  })

  test('affiche l\'historique quand un profil virtuel a été remplacé', async ({ page }) => {
    const replaced: VR = {
      id: 11, project: 1, project_code: 'P-001',
      name: 'Dessinateur junior', default_hourly_rate: '55.00',
      is_active: false,
      replaced_by: 42, replaced_by_name: 'Alice Martin',
      replaced_at: '2026-04-22T10:30:00Z',
      notes: '', created_at: '2026-01-01T00:00:00Z',
    }
    await page.route('**/api/v1/virtual-resources/**', (r) =>
      r.fulfill({ json: { results: [replaced] } }),
    )
    await page.goto('/projects/1?tab=execution/team')
    await expect(page.locator('[data-virtual-row-replaced]')).toHaveCount(1, { timeout: 10_000 })
    await expect(page.locator('[data-virtual-row-replaced]')).toContainText('Dessinateur junior')
    await expect(page.locator('[data-virtual-row-replaced]')).toContainText('Alice Martin')
    await expect(page.locator('[data-virtual-row-replaced]')).toContainText('2026-04-22')
  })
})
