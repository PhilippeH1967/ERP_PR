import { test, expect, type Page } from '@playwright/test'

/**
 * E2E — Saisie de temps « par tâche » (refonte v1.2).
 *
 * Vérifie le contrat UI du picker « + Ajouter une tâche » via route
 * interception (sans backend réel) :
 *   - seules les tâches SAISISSABLES (feuilles, is_chargeable) sont proposées
 *     — les tâches-mères (agrégats) sont exclues ;
 *   - le bouton « Ajouter » est désactivé tant qu'aucune tâche n'est choisie
 *     (la saisie se fait au niveau tâche).
 */

const USER = {
  id: 1, username: 'alice', email: 'alice@x.com',
  first_name: 'Alice', last_name: 'Martin', tenant_id: 1, roles: ['EMPLOYEE'],
}

const PROJECT = { id: 1, code: 'P-001', name: 'Projet Test' }

// Une feuille (saisissable) + une tâche-mère (agrégat, exclue).
const TASKS = [
  { id: 11, phase: 1, phase_name: 'Concept', wbs_code: '1.1', name: 'Feuille saisissable', display_label: 'Feuille saisissable', is_chargeable: true },
  { id: 12, phase: 1, phase_name: 'Concept', wbs_code: '1.2', name: 'Mere agregat', display_label: 'Mere agregat', is_chargeable: false },
]

async function routeAll(page: Page) {
  await page.route('**/api/v1/**', (r) => r.fulfill({ json: { results: [] } }))
  await page.route('**/api/v1/auth/config/', (r) =>
    r.fulfill({ json: { sso_available: false, sso_only: false } }))
  await page.route('**/api/v1/auth/me/', (r) => r.fulfill({ json: USER }))
  await page.route('**/api/v1/projects/**', (r) => {
    const url = r.request().url()
    if (url.includes('/tasks/')) return r.fulfill({ json: { results: TASKS } })
    return r.fulfill({ json: { results: [PROJECT] } })
  })
}

test.describe('Saisie de temps — picker par tâche', () => {
  test.beforeEach(async ({ page }) => {
    await routeAll(page)
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake')
      localStorage.setItem('refresh_token', 'fake')
    })
  })

  test('le picker ne propose que les feuilles et exige une tâche', async ({ page }) => {
    await page.goto('/timesheets')

    // Ouvrir le formulaire d'ajout
    await page.locator('[data-add-task-toggle]').click()

    // « Ajouter » désactivé tant qu'aucun projet/tâche
    await expect(page.locator('[data-add-confirm]')).toBeDisabled()

    // Choisir le projet → charge les tâches
    await page.locator('[data-add-project]').selectOption('1')

    const taskSelect = page.locator('[data-add-task]')
    await expect(taskSelect).toBeVisible({ timeout: 10_000 })
    // Feuille proposée, tâche-mère exclue
    await expect(taskSelect).toContainText('Feuille saisissable')
    await expect(taskSelect).not.toContainText('Mere agregat')

    // Tâche obligatoire : « Ajouter » reste désactivé sans tâche
    await expect(page.locator('[data-add-confirm]')).toBeDisabled()

    // Une fois la feuille choisie → activable
    await taskSelect.selectOption('11')
    await expect(page.locator('[data-add-confirm]')).toBeEnabled()
  })
})
