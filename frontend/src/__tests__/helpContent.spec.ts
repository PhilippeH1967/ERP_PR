import { describe, expect, it } from 'vitest'
import { resolveHelpContext, HELP_FALLBACK_KEY } from '../features/help/helpContent'

describe('resolveHelpContext — aide contextuelle par écran', () => {
  it('fiche projet sans tab → Pilotage', () => {
    const ctx = resolveHelpContext('/projects/15', undefined)
    expect(ctx.key).toBe('project-overview')
    expect(ctx.title).toContain('Pilotage')
    expect(ctx.items.length).toBeGreaterThan(2)
  })

  it('fiche projet ?tab=structure/tasks → Échéancier › Tâches', () => {
    const ctx = resolveHelpContext('/projects/15', 'structure/tasks')
    expect(ctx.key).toBe('project-tasks')
    expect(ctx.title.toLowerCase()).toContain('tâches')
  })

  it('vieux lien ?tab=execution/team → Équipe & charge', () => {
    const ctx = resolveHelpContext('/projects/15', 'execution/team')
    expect(ctx.key).toBe('project-team')
  })

  it('?tab=params → Paramètres du projet', () => {
    const ctx = resolveHelpContext('/projects/15', 'params')
    expect(ctx.key).toBe('project-params')
  })

  it('liste des projets', () => {
    expect(resolveHelpContext('/projects', undefined).key).toBe('projects-list')
  })

  it('feuilles de temps', () => {
    expect(resolveHelpContext('/timesheets', undefined).key).toBe('timesheets')
  })

  it('occupation des ressources (jamais « Planification »)', () => {
    const ctx = resolveHelpContext('/planning', undefined)
    expect(ctx.key).toBe('planning')
    expect(ctx.title).toContain('Occupation')
    expect(ctx.title).not.toContain('Planification')
  })

  it('écran inconnu → fallback générique', () => {
    const ctx = resolveHelpContext('/quelque/chose', undefined)
    expect(ctx.key).toBe(HELP_FALLBACK_KEY)
  })

  it('chaque contexte pointe vers une section du guide', () => {
    const ctx = resolveHelpContext('/projects/15', 'structure/gantt')
    expect(ctx.guideSection).toBe('projects')
  })
})
