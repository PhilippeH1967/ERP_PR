/**
 * Construit l'arbre « Par phase » de l'onglet Équipe : Phase → Tâche →
 * Sous-tâche, avec les **personnes affectées** (allocations) à chaque niveau.
 *
 * Les allocations ciblent une phase XOR une tâche (cf. ResourceAllocation) et
 * portent soit un employé, soit une ressource virtuelle. Fonctions pures,
 * testées indépendamment de la vue.
 */

export interface AllocInput {
  id: number
  employee?: number | null
  employee_name?: string
  virtual_resource?: number | null
  virtual_resource_name?: string
  phase?: number | null
  task?: number | null
  hours_per_week?: string | number
}

export interface TaskInput {
  id: number
  parent: number | null
  name: string
  display_label?: string
  wbs_code?: string
  is_active?: boolean
  order?: number
}

export interface PhaseGroupInput {
  phase_id: number | null
  phase_name: string
  tasks: TaskInput[]
}

export interface PersonChip {
  key: string
  name: string
  kind: 'employee' | 'virtual'
  hours: number
}

export interface TaskTreeNode {
  id: number
  name: string
  wbs_code: string
  is_active: boolean
  people: PersonChip[]
  subtasks: TaskTreeNode[]
}

export interface PhaseTreeNode {
  phase_id: number | null
  phase_name: string
  people: PersonChip[]
  tasks: TaskTreeNode[]
}

function toPerson(a: AllocInput): PersonChip {
  const isVirtual = a.virtual_resource != null
  return {
    key: isVirtual ? `v-${a.virtual_resource}` : `e-${a.employee}`,
    name: isVirtual
      ? a.virtual_resource_name || 'Profil virtuel'
      : a.employee_name || `#${a.employee}`,
    kind: isVirtual ? 'virtual' : 'employee',
    hours: Number(a.hours_per_week || 0),
  }
}

function buildTaskNode(
  task: TaskInput,
  allTasks: TaskInput[],
  allocations: AllocInput[],
): TaskTreeNode {
  return {
    id: task.id,
    name: task.display_label || task.name,
    wbs_code: task.wbs_code || '',
    is_active: task.is_active !== false,
    people: allocations.filter((a) => a.task === task.id).map(toPerson),
    subtasks: allTasks
      .filter((t) => t.parent === task.id)
      .map((t) => buildTaskNode(t, allTasks, allocations)),
  }
}

export function buildPhasePeopleTree(
  groups: PhaseGroupInput[],
  allocations: AllocInput[],
): PhaseTreeNode[] {
  return groups.map((g) => ({
    phase_id: g.phase_id,
    phase_name: g.phase_name,
    // Personnes allouées à la phase directement (task null).
    people: allocations
      .filter((a) => a.phase === g.phase_id && a.task == null)
      .map(toPerson),
    tasks: g.tasks
      .filter((t) => t.parent == null)
      .map((t) => buildTaskNode(t, g.tasks, allocations)),
  }))
}

/** Une phase est visible si elle a au moins une tâche ou une personne. */
export function visiblePhaseNodes(tree: PhaseTreeNode[]): PhaseTreeNode[] {
  return tree.filter((p) => p.tasks.length > 0 || p.people.length > 0)
}

function filterTaskNode(node: TaskTreeNode, q: string): TaskTreeNode | null {
  const subs = node.subtasks
    .map((s) => filterTaskNode(s, q))
    .filter((s): s is TaskTreeNode => s !== null)
  const selfMatch = node.people.some((p) => p.name.toLowerCase().includes(q))
  if (selfMatch || subs.length) {
    return { ...node, subtasks: subs }
  }
  return null
}

/**
 * Filtre l'arbre pour ne garder que les nœuds où une **personne** correspond à
 * la recherche (chemin conservé). Sert au moteur « où est affecté X ».
 */
export function filterTreeByPerson(tree: PhaseTreeNode[], query: string): PhaseTreeNode[] {
  const q = query.trim().toLowerCase()
  if (!q) return tree
  const out: PhaseTreeNode[] = []
  for (const ph of tree) {
    const tasks = ph.tasks
      .map((t) => filterTaskNode(t, q))
      .filter((t): t is TaskTreeNode => t !== null)
    const phMatch = ph.people.some((p) => p.name.toLowerCase().includes(q))
    if (phMatch || tasks.length) {
      out.push({ ...ph, tasks })
    }
  }
  return out
}
