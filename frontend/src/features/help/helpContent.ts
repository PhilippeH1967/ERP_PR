/**
 * Aide contextuelle — source unique du contenu du panneau « ? ».
 * Chaque écran (et chaque onglet de la fiche projet) a un contexte :
 * titre, intro, « ce que vous pouvez faire ici », astuces, et la section du
 * guide complet (/help) correspondante.
 */

export interface HelpItem { title: string; body: string }
export interface HelpContext {
  key: string
  title: string
  intro: string
  items: HelpItem[]
  tips?: string[]
  guideSection: string
}

export const HELP_FALLBACK_KEY = 'default'

const C: Record<string, HelpContext> = {}
function ctx(c: HelpContext) { C[c.key] = c }

/* ── Fiche projet (par onglet) ─────────────────────────────────────────── */
ctx({
  key: 'project-overview', guideSection: 'projects',
  title: '📊 Pilotage du projet',
  intro: "Vue synthétique : où en est le projet, qu'est-ce qui mérite votre attention.",
  items: [
    { title: 'KPI', body: 'Budget des tâches, facturé, % consommé, solde, heures consommées / budget / planifiées.' },
    { title: 'Alertes', body: "Dates incohérentes, tâches sans budget, absence de planification — chaque alerte propose un lien vers l'onglet où corriger." },
    { title: 'Avancement par phase', body: '% heures, % coût et % honoraires par phase, plus le total facturé.' },
    { title: 'Modifier le projet', body: 'Le bouton « Modifier le projet » ouvre l\'onglet ⚙️ Paramètres (nom, dates, responsables, coût de construction).' },
    { title: 'Statut & clôture', body: 'Changer le statut (Actif / En pause / Terminé / Annulé) ; la clôture vérifie une checklist (profils virtuels remplacés, etc.).' },
  ],
  tips: ['Le coût de construction (projets externes) se saisit dans ⚙️ Paramètres et alimente le calcul d\'honoraires « Coût des travaux % ».'],
})
ctx({
  key: 'project-phases', guideSection: 'projects',
  title: '📅 Échéancier › Phases',
  intro: 'Les phases sont des regroupements standard du cabinet (paramétrage admin) : elles ne portent ni budget ni dates propres.',
  items: [
    { title: 'Lecture seule (sauf admin)', body: 'Le jeu de phases est hérité du paramétrage Administration › Phases standard. Seul un admin peut en créer/modifier.' },
    { title: 'Dates dérivées', body: "Les dates d'une phase = min/max des dates de ses tâches. On ne les saisit jamais directement." },
    { title: 'Phases Support', body: 'Les services transversaux (BIM, DD…) sont des phases de type Support avec une tâche imputable.' },
  ],
})
ctx({
  key: 'project-tasks', guideSection: 'projects',
  title: '📅 Échéancier › Tâches',
  intro: "L'outil du quotidien pour structurer et caler le calendrier : tout se passe au niveau tâche / sous-tâche.",
  items: [
    { title: 'Fiche tâche', body: 'Cliquez le nom d\'une tâche pour tout éditer au même endroit : nom, libellé client, phase, dates, budget, affectations, saisie, suppression.' },
    { title: 'Dates inline', body: 'Les colonnes Début / Fin sont éditables directement (fin ≥ début vérifié à la frappe). Les tâches-mères affichent des dates dérivées.' },
    { title: 'Décaler l\'échéancier', body: '« ↔️ Décaler l\'échéancier… » déplace toutes les tâches datées de N jours (négatif = avancer) en un clic.' },
    { title: 'Ajouter des tâches', body: '« + Tâche » (saisie libre) ou « + depuis le modèle » (catalogue standard du cabinet, sans doublon).' },
    { title: 'Fermer / Rouvrir', body: 'Fermer une tâche bloque la saisie de temps pour tout le monde (réversible) ; une tâche-mère ferme tout son groupe.' },
  ],
  tips: ['Le budget et le mode de facturation vivent sur la tâche feuille, jamais sur la phase.'],
})
ctx({
  key: 'project-gantt', guideSection: 'projects',
  title: '📅 Échéancier › Gantt',
  intro: 'Planification fine : barres par tâche, jalons, dépendances.',
  items: [
    { title: 'Barres', body: 'Une barre ne s\'affiche que si la tâche a ses propres dates. Cliquez une barre pour ouvrir la fiche tâche.' },
    { title: 'Jalons', body: 'Ajoutez/modifiez les jalons (slide-over) : nom, date, couleur. Les retards sont détectés automatiquement.' },
    { title: 'Allocations', body: 'Depuis la fiche tâche : affectez employés, équipes ou profils virtuels avec heures/semaine et répartition.' },
    { title: 'Contrôle budget', body: 'Si les heures planifiées dépassent le budget de la tâche, c\'est signalé en rouge — sans bloquer.' },
  ],
})
ctx({
  key: 'project-team', guideSection: 'projects',
  title: '👥 Équipe & charge',
  intro: 'Qui travaille sur quoi, à quelle hauteur — et qui peut imputer du temps.',
  items: [
    { title: 'Par phase / Par personne', body: 'Deux lectures : l\'arbre Phase → Tâche → Sous-tâche avec les personnes, ou la liste par employé avec ses affectations.' },
    { title: '+ Affectation', body: 'Le dialogue unifié pose trois questions : Qui (employé / équipe / profil virtuel) → Où (projet, phase ou tâche) → Combien (h/sem, période).' },
    { title: 'Recherche', body: '« Où une personne est affectée » : tapez un nom, l\'arbre se filtre sur ses affectations.' },
    { title: 'Blocages ciblés', body: 'Vue Par personne : bloquez une personne sur une tâche/phase (cadenas) ou sur tout le projet (« Bloquer (projet) »). Réversible.' },
    { title: 'Fermer (global)', body: 'Vue Par phase : « 🔒 Fermer » bloque la saisie de tout le monde sur une tâche ou toute une phase.' },
  ],
  tips: ['Les profils virtuels se créent/modifient dans ⚙️ Paramètres et se remplacent par un employé réel (les allocations basculent).'],
})
ctx({
  key: 'project-time', guideSection: 'projects',
  title: '⏱ Temps du projet',
  intro: 'Les heures saisies sur le projet, par employé ou par phase.',
  items: [
    { title: 'Pivot', body: 'Basculez entre « Par employé » et « Par phase » ; dépliez les mois pour le détail.' },
    { title: 'Libellés client', body: 'Les rapports destinés au client utilisent les libellés du WBS client, pas la nomenclature interne.' },
  ],
})
ctx({
  key: 'project-finances', guideSection: 'projects',
  title: '💰 Finances du projet',
  intro: 'Budget, honoraires, factures et sous-traitants.',
  items: [
    { title: 'Budget (lecture seule)', body: 'Synthèse par tâche : budget $, heures, facturé, solde. Le budget se MODIFIE dans Échéancier › Tâches (ou la fiche tâche) — une seule porte d\'entrée, pas de double saisie.' },
    { title: 'Honoraires', body: 'Forfait, horaire ou « Coût des travaux % » (le coût de construction se modifie dans ⚙️ Paramètres).' },
    { title: 'Factures', body: 'Les lignes reprennent le WBS client. Une facture émise ne se modifie plus (avoir ou rectificative).' },
    { title: 'Sous-traitants', body: 'Factures ST, retenues, litiges — workflow reçu → autorisé → payé.' },
  ],
})
ctx({
  key: 'project-amendments', guideSection: 'projects',
  title: '📝 Avenants',
  intro: 'Chaque avenant est un mini-contrat rattaché au projet.',
  items: [
    { title: 'Numérotation', body: 'Numéro auto {code projet}-AV-n + numéro externe libre.' },
    { title: 'Portée', body: "Un avenant ajoute/modifie des tâches sur les phases existantes (badge AV-n). L'affectation des ressources se fait ensuite dans le Gantt." },
    { title: 'Workflow', body: 'Brouillon → Soumis → Approuvé/Rejeté (Associé en charge).' },
  ],
})
ctx({
  key: 'project-params', guideSection: 'projects',
  title: '⚙️ Paramètres du projet',
  intro: 'Tout le paramétrage du projet au même endroit.',
  items: [
    { title: 'Informations', body: 'Nom, dates, unité d\'affaires, PM, Associé en charge, coût de construction (projets externes).' },
    { title: 'Profils virtuels', body: 'Créer, modifier, supprimer, ou remplacer par un employé réel.' },
    { title: 'Blocages actifs', body: 'Vue d\'ensemble des blocages de saisie (tâche, phase ou projet) avec déblocage en un clic.' },
    { title: 'Référentiels', body: 'Liens vers Administration : phases standard, tâches standard, équipes.' },
  ],
})

/* ── Autres écrans ─────────────────────────────────────────────────────── */
ctx({
  key: 'projects-list', guideSection: 'projects',
  title: '📁 Projets',
  intro: 'Tous les projets auxquels vous avez accès.',
  items: [
    { title: 'Recherche & filtres', body: 'Recherche live (code, nom) et filtres statut / client / unité d\'affaires.' },
    { title: 'Nouveau projet', body: 'Le wizard guide en 5 étapes : identification (dont services transversaux), phases standard, ressources, sous-traitants, confirmation.' },
  ],
})
ctx({
  key: 'timesheets', guideSection: 'timesheets',
  title: '🕐 Feuilles de temps',
  intro: 'Saisie hebdomadaire des heures par tâche.',
  items: [
    { title: 'Saisie', body: 'Choisissez le projet puis la tâche (feuilles uniquement). Les tâches obligatoires (Congés, Formation, Maladie) sont toujours affichées.' },
    { title: 'Favoris', body: 'Épinglez vos tâches récurrentes pour les retrouver chaque semaine.' },
    { title: 'Soumission', body: 'Soumettez la semaine : validation PM → Finance → Paie. Les heures validées ne sont plus modifiables.' },
    { title: 'Blocages', body: 'Une tâche fermée ou un blocage posé par votre PM empêche la saisie (message explicite).' },
  ],
})
ctx({
  key: 'leaves', guideSection: 'leaves',
  title: '🏖️ Congés',
  intro: 'Demandes d\'absence et soldes.',
  items: [
    { title: 'Demande', body: '7 types (Vacances, Maladie, Personnel…). Pas de chevauchement entre deux demandes.' },
    { title: 'Validation', body: 'Approbation RH avant impact sur l\'occupation ; l\'approbation crée les entrées de temps.' },
  ],
})
ctx({
  key: 'planning', guideSection: 'planning',
  title: '📅 Occupation des ressources',
  intro: 'Charge de l\'équipe : qui est planifié où, sur quelles semaines.',
  items: [
    { title: 'Vue Gantt / tableau', body: 'Par employé : allocations, heures planifiées vs contrat, statut de charge (normal, sous-charge, surcharge, critique).' },
    { title: 'Alertes', body: 'Surcharges et sous-charges des 4 prochaines semaines.' },
  ],
})
ctx({
  key: 'billing', guideSection: 'billing',
  title: '📄 Facturation',
  intro: 'Factures clients, paiements et taxes.',
  items: [
    { title: 'Cycle', body: 'Brouillon → Soumise → Approuvée → Envoyée → Payée. Une facture émise ne se modifie plus.' },
    { title: 'Taxes', body: 'Schémas fiscaux par province (TPS+TVQ, TVH…), calcul automatique.' },
  ],
})
ctx({
  key: 'dashboard', guideSection: 'dashboard',
  title: '📊 Tableau de bord',
  intro: 'KPIs adaptés à votre rôle.',
  items: [
    { title: 'Par rôle', body: 'PM : heures, ratio CA/salaires, carnet. Finance : impayés, dépenses en attente. Admin : santé du système.' },
  ],
})
ctx({
  key: 'admin', guideSection: 'faq',
  title: '🛠 Administration',
  intro: 'Paramétrage global du cabinet (admin).',
  items: [
    { title: 'Référentiels', body: 'Phases standard (héritées par tous les projets), catalogue de tâches standard, équipes réutilisables, schémas fiscaux.' },
    { title: 'Périodes', body: 'Verrouillage des périodes de paie et exceptions.' },
  ],
})
ctx({
  key: HELP_FALLBACK_KEY, guideSection: 'welcome',
  title: '❓ Aide',
  intro: 'Pas d\'aide spécifique pour cet écran — voici l\'essentiel.',
  items: [
    { title: 'Guide complet', body: 'Le Centre d\'aide décrit chaque module, écran par écran, selon votre rôle.' },
    { title: 'Navigation', body: 'La barre latérale regroupe vos accès par domaine (Mon travail, Pilotage, Finance…).' },
  ],
})

/* ── Résolution ────────────────────────────────────────────────────────── */
const PROJECT_TAB_MAP: Record<string, string> = {
  overview: 'project-overview',
  phases: 'project-phases',
  tasks: 'project-tasks',
  gantt: 'project-gantt',
  team: 'project-team',
  time: 'project-time',
  budget: 'project-finances',
  invoices: 'project-finances',
  st: 'project-finances',
  finances: 'project-finances',
  amendments: 'project-amendments',
  params: 'project-params',
}

const PATH_MAP: Array<[RegExp, string]> = [
  [/^\/projects\/?$/, 'projects-list'],
  [/^\/timesheets/, 'timesheets'],
  [/^\/leaves/, 'leaves'],
  [/^\/planning/, 'planning'],
  [/^\/(billing|invoices|payments)/, 'billing'],
  [/^\/admin/, 'admin'],
  [/^\/(dashboard)?$/, 'dashboard'],
]

export function resolveHelpContext(path: string, tabQuery: string | undefined): HelpContext {
  if (/^\/projects\/\d+/.test(path)) {
    const sub = (tabQuery || 'overview').split('/').pop() || 'overview'
    return C[PROJECT_TAB_MAP[sub] || 'project-overview']!
  }
  for (const [re, key] of PATH_MAP) {
    if (re.test(path)) return C[key]!
  }
  return C[HELP_FALLBACK_KEY]!
}
