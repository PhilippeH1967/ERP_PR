<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuth } from '@/shared/composables/useAuth'

const { currentUser } = useAuth()

const activeSection = ref('welcome')

const userRoles = computed(() => currentUser.value?.roles || [])
const hasRole = (role: string) => userRoles.value.includes(role)

interface Section { key: string; label: string; icon: string; roles?: string[] }

const allSections: Section[] = [
  { key: 'welcome', label: 'Bienvenue', icon: '👋' },
  { key: 'timesheets', label: 'Feuilles de temps', icon: '🕐' },
  { key: 'leaves', label: 'Conges', icon: '🏖️' },
  { key: 'projects', label: 'Projets', icon: '📁' },
  { key: 'expenses', label: 'Depenses', icon: '🧾' },
  { key: 'approvals', label: 'Approbations', icon: '✅', roles: ['PM', 'PROJECT_DIRECTOR', 'FINANCE', 'PAIE', 'ADMIN'] },
  { key: 'billing', label: 'Facturation', icon: '📄', roles: ['FINANCE', 'PM', 'PROJECT_DIRECTOR', 'ADMIN'] },
  { key: 'planning', label: 'Planification', icon: '📅' },
  { key: 'dashboard', label: 'Tableau de bord', icon: '📊' },
  { key: 'faq', label: 'FAQ', icon: '❓' },
]

const sections = computed(() =>
  allSections.filter(s => {
    if (!s.roles) return true
    return s.roles.some(r => hasRole(r)) || hasRole('ADMIN')
  }),
)
</script>

<template>
  <div class="help-layout">
    <!-- Sidebar -->
    <aside class="help-sidebar">
      <div class="help-sidebar-header">
        <span class="help-title">Guide utilisateur</span>
        <span class="help-subtitle">PR|ERP</span>
      </div>
      <nav class="help-nav">
        <button
          v-for="s in sections"
          :key="s.key"
          class="help-nav-item"
          :class="{ active: activeSection === s.key }"
          @click="activeSection = s.key"
        >
          <span class="help-nav-icon">{{ s.icon }}</span>
          <span>{{ s.label }}</span>
        </button>
      </nav>
    </aside>

    <!-- Content -->
    <main class="help-content">

      <!-- Bienvenue -->
      <template v-if="activeSection === 'welcome'">
        <h1>Bienvenue dans PR|ERP</h1>
        <p class="help-intro">
          PR|ERP est votre outil de gestion integre pour la gestion de projets, la saisie de temps,
          la facturation, les depenses et la planification des ressources.
          Ce guide vous accompagne dans l'utilisation quotidienne de l'application.
        </p>

        <div class="help-cards">
          <div class="help-card" @click="activeSection = 'timesheets'">
            <span class="help-card-icon">🕐</span>
            <h3>Feuilles de temps</h3>
            <p>Saisir et soumettre vos heures hebdomadaires</p>
          </div>
          <div class="help-card" @click="activeSection = 'leaves'">
            <span class="help-card-icon">🏖️</span>
            <h3>Conges</h3>
            <p>Demander un conge et consulter vos soldes</p>
          </div>
          <div class="help-card" @click="activeSection = 'projects'">
            <span class="help-card-icon">📁</span>
            <h3>Projets</h3>
            <p>Consulter vos projets et leur avancement</p>
          </div>
          <div class="help-card" @click="activeSection = 'expenses'">
            <span class="help-card-icon">🧾</span>
            <h3>Depenses</h3>
            <p>Soumettre une note de frais avec justificatif</p>
          </div>
          <div class="help-card" @click="activeSection = 'dashboard'">
            <span class="help-card-icon">📊</span>
            <h3>Tableau de bord</h3>
            <p>Vue d'ensemble et indicateurs cles</p>
          </div>
          <div class="help-card" @click="activeSection = 'faq'">
            <span class="help-card-icon">❓</span>
            <h3>FAQ</h3>
            <p>Reponses aux questions frequentes</p>
          </div>
        </div>

        <h2>Vos roles</h2>
        <p>Vous avez acces aux fonctionnalites suivantes selon vos roles :</p>
        <div class="role-badges">
          <span v-for="role in userRoles" :key="role" class="role-badge">{{ role }}</span>
        </div>

        <div class="help-tip">
          <strong>Astuce :</strong> La barre de navigation a gauche vous donne acces rapide a toutes les sections.
          Le menu utilisateur (en haut a droite) permet de changer la langue (FR/EN) et de vous deconnecter.
        </div>
      </template>

      <!-- Feuilles de temps -->
      <template v-if="activeSection === 'timesheets'">
        <h1>Feuilles de temps</h1>
        <p class="help-intro">Chaque semaine, vous devez saisir vos heures de travail par projet et par tache. L'objectif : moins de 5 minutes par semaine.</p>

        <h2>Saisir vos heures</h2>
        <ol class="help-steps">
          <li>
            <strong>Ouvrir la grille</strong> — Cliquez sur <em>Feuilles de temps</em> dans le menu.
            Votre grille hebdomadaire s'affiche avec uniquement les projets et taches auxquels vous etes affecte.
          </li>
          <li>
            <strong>Entrer les heures</strong> — Pour chaque jour, saisissez le nombre d'heures travaillees dans la cellule correspondant au projet/tache.
            Les libelles affiches sont ceux definis par le client (libelles client).
          </li>
          <li>
            <strong>Verifier les totaux</strong> — Le total journalier s'affiche en bas de chaque colonne.
            Un indicateur visuel vous alerte si le total differe de votre norme contractuelle (7,5h ou 8h).
          </li>
          <li>
            <strong>Enregistrer en brouillon</strong> — Vos heures sont sauvegardees automatiquement. Vous pouvez modifier vos entrees a tout moment avant soumission.
          </li>
          <li>
            <strong>Soumettre la semaine</strong> — Une fois satisfait, cliquez sur <em>Soumettre</em>.
            Vos heures passent en revision et ne peuvent plus etre modifiees par vous.
          </li>
        </ol>

        <h2>Cycle d'approbation</h2>
        <p>Vos heures suivent un processus en 3 niveaux :</p>
        <div class="help-workflow">
          <div class="wf-step"><span class="wf-badge wf-draft">Brouillon</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-submitted">Soumis</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-pm">PM approuve</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-finance">Finance valide</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-paie">Paie validee</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-locked">Verrouillee</span></div>
        </div>

        <div class="help-tip">
          <strong>Important :</strong> Si votre feuille est rejetee a n'importe quel niveau, elle revient en <em>Brouillon</em> avec un motif visible.
          Corrigez les heures concernees et resoumettez.
        </div>

        <h2>Statistiques hebdomadaires</h2>
        <p>En haut de la grille, vous voyez :</p>
        <ul>
          <li><strong>Heures contrat</strong> — Votre nombre d'heures contractuelles par semaine</li>
          <li><strong>Moyenne 4 semaines</strong> — Votre moyenne glissante sur les 4 dernieres semaines</li>
          <li><strong>Taux facturable</strong> — Pourcentage de vos heures sur des taches facturables</li>
        </ul>

        <h2>Favoris et raccourcis</h2>
        <p>
          Si vous travaillez regulierement sur les memes projets, utilisez les <strong>favoris</strong> pour les garder
          en haut de votre grille. Cliquez sur l'etoile a cote du nom du projet.
        </p>
      </template>

      <!-- Conges -->
      <template v-if="activeSection === 'leaves'">
        <h1>Conges</h1>
        <p class="help-intro">Gerez vos demandes de conge et consultez vos soldes disponibles.</p>

        <h2>Types de conges disponibles</h2>
        <table class="help-table">
          <thead><tr><th>Type</th><th>Description</th></tr></thead>
          <tbody>
            <tr><td>Vacances annuelles</td><td>Jours de vacances selon votre anciennete</td></tr>
            <tr><td>Conge maladie</td><td>Journees maladie (avec ou sans certificat selon la duree)</td></tr>
            <tr><td>Conge personnel</td><td>Journees personnelles prevues a la convention</td></tr>
            <tr><td>Jours feries</td><td>Jours feries du Quebec (automatiques)</td></tr>
            <tr><td>Conge parental</td><td>Conge maternite/paternite/adoption</td></tr>
            <tr><td>Conge sans solde</td><td>Absence non remuneree, sur approbation</td></tr>
            <tr><td>Conge special</td><td>Deces, mariage, demenagement, etc.</td></tr>
          </tbody>
        </table>

        <h2>Faire une demande</h2>
        <ol class="help-steps">
          <li>Allez dans <em>Conges</em> depuis le menu de navigation.</li>
          <li>Cliquez sur <strong>Nouvelle demande</strong>.</li>
          <li>Selectionnez le type de conge, les dates de debut et fin, et ajoutez une note si necessaire.</li>
          <li>Soumettez la demande. Votre gestionnaire recevra une notification.</li>
        </ol>

        <h2>Approbation et impact</h2>
        <p>
          Une fois votre demande approuvee, le systeme cree automatiquement les entrees de temps correspondantes
          dans votre feuille de temps (type conge). Votre solde de conge est debite en consequence.
        </p>

        <h2>Consulter vos soldes</h2>
        <p>
          En haut de la page des conges, vos <strong>soldes actuels</strong> sont affiches par type :
          jours acquis, jours utilises, et solde restant.
        </p>
      </template>

      <!-- Projets -->
      <template v-if="activeSection === 'projects'">
        <h1>Projets</h1>
        <p class="help-intro">Consultez vos projets, leur avancement et leur structure.</p>

        <h2>Liste des projets</h2>
        <p>
          La page <em>Projets</em> affiche tous les projets auxquels vous avez acces.
          Utilisez les filtres (statut, client, unite d'affaires) pour affiner la liste.
        </p>

        <h2>Fiche projet (12 onglets)</h2>
        <p>Chaque projet dispose d'une fiche detaillee avec les onglets suivants :</p>
        <table class="help-table">
          <thead><tr><th>Onglet</th><th>Contenu</th></tr></thead>
          <tbody>
            <tr><td><strong>Resume</strong></td><td>Informations generales, dates, responsables, statut</td></tr>
            <tr><td><strong>WBS</strong></td><td>Structure de decoupage : phases, taches, sous-taches</td></tr>
            <tr><td><strong>Budget</strong></td><td>Budget par phase, montants factures, restant</td></tr>
            <tr><td><strong>Equipe</strong></td><td>Membres affectes et leurs roles</td></tr>
            <tr><td><strong>Temps</strong></td><td>Heures saisies par phase et par personne</td></tr>
            <tr><td><strong>Facturation</strong></td><td>Factures emises, ratio CA/Salaires</td></tr>
            <tr><td><strong>Depenses</strong></td><td>Notes de frais liees au projet</td></tr>
            <tr><td><strong>Sous-traitants</strong></td><td>Factures ST, budgets, retenues</td></tr>
            <tr><td><strong>Gantt</strong></td><td>Vue chronologique des phases et jalons</td></tr>
            <tr><td><strong>Documents</strong></td><td>Pieces jointes au projet</td></tr>
            <tr><td><strong>Historique</strong></td><td>Journal de toutes les modifications</td></tr>
            <tr><td><strong>Avenants</strong></td><td>Modifications contractuelles et leur impact</td></tr>
          </tbody>
        </table>

        <h2 v-if="hasRole('PM') || hasRole('ADMIN')">Creer un projet (PM)</h2>
        <div v-if="hasRole('PM') || hasRole('ADMIN')">
          <p>La creation de projet suit un assistant en 5 etapes :</p>
          <ol class="help-steps">
            <li><strong>Metadonnees</strong> — Nom, client, type de contrat, dates, responsables (PM, Associe en charge, Approbateur facture)</li>
            <li><strong>Phases / WBS</strong> — Definir les phases de realisation et services transversaux. Un template par type de contrat est propose.</li>
            <li><strong>Budget</strong> — Heures et couts par phase/tache, mode de facturation (forfait ou horaire)</li>
            <li><strong>Ressources & Planification</strong> — Affecter des profils virtuels par phase, definir les dates dans le Gantt</li>
            <li><strong>Sous-traitants</strong> — Configurer les budgets ST (optionnel, peut etre complete plus tard)</li>
          </ol>
        </div>

        <h2>Vue Gantt</h2>
        <p>
          Le Gantt interactif affiche les phases du projet sur une timeline.
          Vous pouvez zoomer (mois, trimestre, annee), voir les jalons et les dependances entre phases.
        </p>
      </template>

      <!-- Depenses -->
      <template v-if="activeSection === 'expenses'">
        <h1>Depenses</h1>
        <p class="help-intro">Soumettez vos notes de frais avec justificatifs pour remboursement.</p>

        <h2>Creer une note de frais</h2>
        <ol class="help-steps">
          <li>Allez dans <em>Depenses</em> depuis le menu.</li>
          <li>Cliquez sur <strong>Nouvelle depense</strong>.</li>
          <li>Remplissez : date, montant, categorie, projet associe, et description.</li>
          <li>Cochez <em>Refacturable au client</em> si la depense doit etre reportee sur la facture client.</li>
          <li><strong>Joignez le recu</strong> (photo ou PDF) — obligatoire pour chaque ligne.</li>
          <li>Soumettez la note de frais.</li>
        </ol>

        <h2>Categories de depenses</h2>
        <p>15 categories sont disponibles, incluant :</p>
        <div class="help-tag-list">
          <span class="help-tag">Transport</span>
          <span class="help-tag">Repas</span>
          <span class="help-tag">Hebergement</span>
          <span class="help-tag">Kilometrage</span>
          <span class="help-tag">Fournitures</span>
          <span class="help-tag">Telecommunications</span>
          <span class="help-tag">Formation</span>
          <span class="help-tag">Stationnement</span>
          <span class="help-tag">Impression / Reprographie</span>
          <span class="help-tag">Equipement</span>
          <span class="help-tag">Logiciels</span>
          <span class="help-tag">Representation</span>
          <span class="help-tag">Poste / Messagerie</span>
          <span class="help-tag">Frais professionnels</span>
          <span class="help-tag">Divers</span>
        </div>

        <h2>Cycle d'approbation</h2>
        <div class="help-workflow">
          <div class="wf-step"><span class="wf-badge wf-draft">Brouillon</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-submitted">Soumis</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-pm">Approbateur valide</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-finance">Finance valide</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-paie">Paiement</span></div>
        </div>
      </template>

      <!-- Approbations -->
      <template v-if="activeSection === 'approvals'">
        <h1>Approbations</h1>
        <p class="help-intro">En tant qu'approbateur, vous validez les feuilles de temps et les depenses de vos equipes.</p>

        <h2>Approbation des feuilles de temps</h2>

        <h3 v-if="hasRole('PM') || hasRole('ADMIN')">Chefs de projet (PM)</h3>
        <div v-if="hasRole('PM') || hasRole('ADMIN')">
          <ul>
            <li>Vous approuvez les entrees <strong>individuellement</strong> (par entree, pas par feuille entiere)</li>
            <li>Code couleur : <span style="color: #3B82F6; font-weight: 600;">bleu</span> = vos projets,
              <span style="color: #10B981; font-weight: 600;">vert</span> = deja approuve,
              <span style="color: #9CA3AF; font-weight: 600;">gris</span> = projets d'un autre PM</li>
            <li>Vous pouvez rejeter une entree avec un motif — l'employe sera notifie</li>
          </ul>
        </div>

        <h3 v-if="hasRole('FINANCE') || hasRole('ADMIN')">Finance</h3>
        <div v-if="hasRole('FINANCE') || hasRole('ADMIN')">
          <ul>
            <li>Validation de 2e niveau apres le PM</li>
            <li>Possibilite de corriger retroactivement des entrees validees (avec piste d'audit)</li>
            <li>Transfert d'heures entre projets si necessaire</li>
          </ul>
        </div>

        <h3 v-if="hasRole('PAIE') || hasRole('ADMIN')">Paie</h3>
        <div v-if="hasRole('PAIE') || hasRole('ADMIN')">
          <ul>
            <li>Validation de 3e niveau avec <strong>11 controles automatiques</strong></li>
            <li>Les controles detectent : heures incompletes, heures supplementaires excessives, maladie + travail le meme jour, tendances inhabituelles, etc.</li>
            <li>Validation individuelle ou en lot possible</li>
            <li>Gestion du gel de periode (verrouillage global des feuilles de temps)</li>
          </ul>
        </div>

        <h2>Les 11 controles paie</h2>
        <table class="help-table">
          <thead><tr><th>Controle</th><th>Severite</th><th>Description</th></tr></thead>
          <tbody>
            <tr><td>Heures incompletes</td><td class="sev-warning">Avertissement</td><td>Total &lt; heures contrat sans absence declaree</td></tr>
            <tr><td>Heures supp + maladie</td><td class="sev-error">Erreur</td><td>Heures supp la meme semaine qu'un conge maladie</td></tr>
            <tr><td>Heures supp + conge</td><td class="sev-warning">Avertissement</td><td>Heures supp la meme semaine qu'un autre conge</td></tr>
            <tr><td>Heures supplementaires</td><td class="sev-warning">Avert./Erreur</td><td>Depassement seuil (erreur si &gt;10h supp)</td></tr>
            <tr><td>Journee &gt; 10h</td><td class="sev-warning">Avertissement</td><td>Plus de 10 heures sur une seule journee</td></tr>
            <tr><td>Travail fin de semaine</td><td class="sev-warning">Avertissement</td><td>Heures saisies samedi ou dimanche</td></tr>
            <tr><td>Maladie + travail</td><td class="sev-error">Erreur</td><td>Conge maladie et heures le meme jour</td></tr>
            <tr><td>Tendance inhabituelle</td><td class="sev-info">Info</td><td>Ecart &gt;20% par rapport a la moyenne 4 semaines</td></tr>
            <tr><td>Supp consecutives</td><td class="sev-error">Erreur</td><td>3+ semaines consecutives d'heures supplementaires</td></tr>
            <tr><td>PM non approuve</td><td class="sev-error">Erreur</td><td>Entrees encore en attente d'approbation PM</td></tr>
            <tr><td>Maximum legal 50h</td><td class="sev-error">Erreur</td><td>Total hebdomadaire depasse 50h (LNT Quebec)</td></tr>
          </tbody>
        </table>
      </template>

      <!-- Facturation -->
      <template v-if="activeSection === 'billing'">
        <h1>Facturation</h1>
        <p class="help-intro">Creez, suivez et gerez les factures clients.</p>

        <h2>Cycle de vie d'une facture</h2>
        <div class="help-workflow">
          <div class="wf-step"><span class="wf-badge wf-draft">Brouillon</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-submitted">Soumise</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-pm">Approuvee</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-finance">Envoyee</span><span class="wf-arrow">&rarr;</span></div>
          <div class="wf-step"><span class="wf-badge wf-locked">Payee</span></div>
        </div>

        <h2 v-if="hasRole('FINANCE') || hasRole('ADMIN')">Preparation d'une facture (Finance)</h2>
        <div v-if="hasRole('FINANCE') || hasRole('ADMIN')">
          <p>L'ecran de preparation affiche 7 colonnes par phase/tache :</p>
          <table class="help-table">
            <thead><tr><th>#</th><th>Colonne</th><th>Description</th></tr></thead>
            <tbody>
              <tr><td>1</td><td>Livrable</td><td>Nom de la phase/tache</td></tr>
              <tr><td>2</td><td>Montant contrat</td><td>Valeur contractuelle totale</td></tr>
              <tr><td>3</td><td>Facture a ce jour</td><td>Cumul des factures precedentes</td></tr>
              <tr><td>4</td><td>% avancement facturation</td><td>Progression de la facturation</td></tr>
              <tr><td>5</td><td>% avancement heures</td><td>Heures consommees vs budget</td></tr>
              <tr><td>6</td><td>A facturer ce mois</td><td>Montant modifiable pour ce cycle</td></tr>
              <tr><td>7</td><td>% apres facturation</td><td>Avancement projete apres ce cycle</td></tr>
            </tbody>
          </table>
          <p>
            Le bandeau <strong>ratio CA/Salaires</strong> se met a jour en temps reel
            pendant la preparation. Des alertes visuelles signalent les ecarts &gt;10 points
            entre l'avancement heures et la facturation.
          </p>
        </div>

        <h2>Schemas fiscaux</h2>
        <p>6 schemas fiscaux sont configures :</p>
        <table class="help-table">
          <thead><tr><th>Schema</th><th>Taxes applicables</th></tr></thead>
          <tbody>
            <tr><td>Quebec (QC)</td><td>TPS 5% + TVQ 9,975%</td></tr>
            <tr><td>Ontario (ON)</td><td>TVH 13%</td></tr>
            <tr><td>Alberta (AB)</td><td>TPS 5%</td></tr>
            <tr><td>Colombie-Britannique (BC)</td><td>TPS 5% + TVP 7%</td></tr>
            <tr><td>France (FR)</td><td>TVA 20%</td></tr>
            <tr><td>Exonere</td><td>Aucune taxe</td></tr>
          </tbody>
        </table>

        <h2 v-if="hasRole('PM') || hasRole('PROJECT_DIRECTOR') || hasRole('ADMIN')">Approbation (PM / Directeur)</h2>
        <div v-if="hasRole('PM') || hasRole('PROJECT_DIRECTOR') || hasRole('ADMIN')">
          <p>
            Les factures en attente apparaissent dans votre file d'approbation.
            Vous pouvez previsualiser le brouillon avant d'approuver ou de rejeter.
          </p>
        </div>
      </template>

      <!-- Planification -->
      <template v-if="activeSection === 'planning'">
        <h1>Planification</h1>
        <p class="help-intro">Visualisez l'allocation des ressources et la disponibilite des equipes.</p>

        <h2>Vue globale des ressources</h2>
        <p>
          La page <em>Planification</em> affiche l'allocation de chaque employe par projet et par semaine.
          Les indicateurs de charge permettent d'identifier :
        </p>
        <ul>
          <li><span style="color: #DC2626; font-weight: 600;">Rouge</span> — Surcharge : plus de 100% d'allocation</li>
          <li><span style="color: #F59E0B; font-weight: 600;">Jaune</span> — Attention : entre 80% et 100%</li>
          <li><span style="color: #10B981; font-weight: 600;">Vert</span> — Disponible : moins de 80%</li>
        </ul>

        <h2>Gantt projet</h2>
        <p>
          Depuis un projet, l'onglet <em>Gantt</em> affiche les phases sur une timeline avec :
        </p>
        <ul>
          <li>Barres de couleur representant la duree de chaque phase</li>
          <li>Jalons (losanges) pour les dates cles</li>
          <li>Dependances entre phases (fin-debut, debut-debut)</li>
          <li>3 niveaux de zoom : mois, trimestre, annee</li>
        </ul>

        <h2>Alertes de charge</h2>
        <p>
          Le systeme detecte automatiquement les employes en surcharge ou sous-charge
          et affiche des alertes sur la page de planification.
        </p>

        <h2>Disponibilite</h2>
        <p>
          La disponibilite est calculee automatiquement a partir de vos heures contractuelles
          moins les conges approuves et jours feries.
        </p>
      </template>

      <!-- Tableau de bord -->
      <template v-if="activeSection === 'dashboard'">
        <h1>Tableau de bord</h1>
        <p class="help-intro">Votre tableau de bord est adapte a votre role pour afficher les informations les plus pertinentes.</p>

        <h2>Par role</h2>
        <table class="help-table">
          <thead><tr><th>Role</th><th>Indicateurs affiches</th></tr></thead>
          <tbody>
            <tr><td><strong>Employe</strong></td><td>Heures cette semaine, statut feuille de temps, conges restants, depenses en cours</td></tr>
            <tr><td><strong>Chef de projet (PM)</strong></td><td>Sante des projets (vert/jaune/rouge), ratio CA/Salaires, taux de facturation, carnet de commandes, approbations en attente</td></tr>
            <tr><td><strong>Finance</strong></td><td>Factures en attente, aging (30/60/90 jours), feuilles de temps a valider, exports a traiter</td></tr>
            <tr><td><strong>Directeur</strong></td><td>Vue portfolio, marges globales, taux d'utilisation, projets en alerte</td></tr>
            <tr><td><strong>Admin</strong></td><td>Sante systeme, taux d'adoption par BU, temps de reponse, erreurs</td></tr>
          </tbody>
        </table>

        <h2>Rapports</h2>
        <p>
          La section <em>Rapports</em> permet de generer des rapports d'heures groupables par :
        </p>
        <ul>
          <li><strong>Projet</strong> — Heures par phase pour un projet donne</li>
          <li><strong>Employe</strong> — Toutes les heures d'un employe par projet</li>
          <li><strong>Unite d'affaires</strong> — Synthese par BU</li>
        </ul>
        <p>Tous les rapports sont exportables en CSV.</p>
      </template>

      <!-- FAQ -->
      <template v-if="activeSection === 'faq'">
        <h1>Questions frequentes</h1>

        <div class="faq-item">
          <h3>Je ne vois pas un projet dans ma feuille de temps</h3>
          <p>Vous ne voyez que les projets auxquels vous etes affecte. Demandez a votre chef de projet de vous ajouter a l'equipe du projet.</p>
        </div>

        <div class="faq-item">
          <h3>Ma feuille de temps a ete rejetee, que faire ?</h3>
          <p>Ouvrez votre feuille de temps — le motif de rejet est affiche. Corrigez les entrees concernees et resoumettez.</p>
        </div>

        <div class="faq-item">
          <h3>Comment corriger des heures deja approuvees ?</h3>
          <p>Seule l'equipe Finance peut corriger des heures deja validees. Contactez votre responsable Finance en precisant le projet, la date et la correction souhaitee.</p>
        </div>

        <div class="faq-item">
          <h3>Comment savoir si une depense est refacturable ?</h3>
          <p>C'est le chef de projet qui definit quelles categories de depenses sont refacturables au client pour chaque projet. En cas de doute, demandez a votre PM.</p>
        </div>

        <div class="faq-item">
          <h3>Que signifie le symbole "$" sur une cellule de temps ?</h3>
          <p>Le badge "$" indique que ces heures ont ete incluses dans une facture envoyee au client. Elles ne seront pas facturees une deuxieme fois.</p>
        </div>

        <div class="faq-item">
          <h3>La periode est verrouillee, je ne peux plus saisir</h3>
          <p>
            Les periodes sont verrouillees apres le cycle de paie. Si vous avez besoin d'une correction,
            contactez l'equipe Finance ou Paie qui peut accorder un deverrouillage temporaire.
          </p>
        </div>

        <div class="faq-item">
          <h3>Comment changer la langue de l'application ?</h3>
          <p>Cliquez sur le bouton <strong>EN</strong> ou <strong>FR</strong> dans la barre superieure pour basculer entre le francais et l'anglais.</p>
        </div>

        <div class="faq-item">
          <h3>A qui m'adresser pour un probleme technique ?</h3>
          <p>Contactez l'equipe d'administration systeme via le canal habituel. Ils ont acces aux journaux d'audit et a la configuration du systeme.</p>
        </div>
      </template>

      <div class="help-footer">
        <p>PR|ERP v1.2.000 — Guide utilisateur</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.help-layout { display: flex; min-height: calc(100vh - 56px); margin: -24px; }

.help-sidebar { width: 220px; min-width: 220px; background: #1E293B; color: white; padding: 20px 0; }
.help-sidebar-header { padding: 0 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.help-title { display: block; font-size: 15px; font-weight: 700; color: white; }
.help-subtitle { font-size: 10px; color: #94A3B8; }

.help-nav { display: flex; flex-direction: column; padding-top: 8px; }
.help-nav-item {
  display: flex; align-items: center; gap: 10px; padding: 10px 20px;
  font-size: 13px; color: #94A3B8; background: none; border: none;
  text-align: left; cursor: pointer; transition: all 0.15s;
}
.help-nav-item:hover { color: white; background: rgba(255,255,255,0.05); }
.help-nav-item.active { color: white; background: rgba(59,130,246,0.2); border-right: 3px solid #3B82F6; font-weight: 600; }
.help-nav-icon { font-size: 16px; width: 20px; text-align: center; }

.help-content { flex: 1; padding: 32px 40px; max-width: 860px; overflow-y: auto; }
.help-content h1 { font-size: 24px; font-weight: 700; color: var(--color-gray-900); margin-bottom: 8px; padding-bottom: 12px; border-bottom: 2px solid var(--color-gray-200); }
.help-content h2 { font-size: 16px; font-weight: 600; color: var(--color-gray-800); margin: 28px 0 12px; }
.help-content h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-700); margin: 16px 0 8px; }
.help-intro { font-size: 14px; color: var(--color-gray-600); line-height: 1.7; margin-bottom: 24px; }
.help-content p { font-size: 13px; color: var(--color-gray-700); line-height: 1.6; margin-bottom: 12px; }
.help-content ul, .help-content ol { padding-left: 20px; margin-bottom: 16px; }
.help-content li { font-size: 13px; color: var(--color-gray-700); margin-bottom: 6px; line-height: 1.5; }

.help-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px; }
.help-card {
  background: white; border: 1px solid var(--color-gray-200); border-radius: 10px;
  padding: 20px; cursor: pointer; transition: all 0.2s;
}
.help-card:hover { border-color: var(--color-primary); box-shadow: 0 2px 8px rgba(59,130,246,0.1); transform: translateY(-1px); }
.help-card-icon { font-size: 28px; display: block; margin-bottom: 8px; }
.help-card h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin: 0 0 4px; }
.help-card p { font-size: 12px; color: var(--color-gray-500); margin: 0; }

.role-badges { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.role-badge { padding: 4px 12px; background: var(--color-primary-light, #EFF6FF); color: var(--color-primary); font-size: 11px; font-weight: 600; border-radius: 20px; }

.help-tip {
  background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px;
  padding: 12px 16px; font-size: 13px; color: #166534; margin: 16px 0;
}

.help-steps { counter-reset: step; list-style: none; padding-left: 0; }
.help-steps li {
  counter-increment: step; position: relative; padding: 12px 16px 12px 48px;
  margin-bottom: 8px; background: white; border: 1px solid var(--color-gray-200);
  border-radius: 8px; font-size: 13px; color: var(--color-gray-700); line-height: 1.5;
}
.help-steps li::before {
  content: counter(step); position: absolute; left: 14px; top: 12px;
  width: 24px; height: 24px; background: var(--color-primary); color: white;
  border-radius: 50%; font-size: 12px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

.help-workflow { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; margin: 12px 0 20px; }
.wf-step { display: flex; align-items: center; gap: 4px; }
.wf-badge { padding: 5px 12px; border-radius: 16px; font-size: 11px; font-weight: 600; white-space: nowrap; }
.wf-arrow { color: var(--color-gray-400); font-size: 16px; }
.wf-draft { background: #F3F4F6; color: #374151; }
.wf-submitted { background: #DBEAFE; color: #1D4ED8; }
.wf-pm { background: #D1FAE5; color: #065F46; }
.wf-finance { background: #FEF3C7; color: #92400E; }
.wf-paie { background: #E0E7FF; color: #3730A3; }
.wf-locked { background: #F3E8FF; color: #6B21A8; }

.help-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px; }
.help-table th { padding: 8px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200); text-align: left; }
.help-table td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); }
.sev-error { color: #DC2626; font-weight: 600; }
.sev-warning { color: #F59E0B; font-weight: 600; }
.sev-info { color: #3B82F6; font-weight: 600; }

.help-tag-list { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.help-tag { padding: 3px 10px; background: var(--color-gray-100); color: var(--color-gray-600); font-size: 11px; border-radius: 12px; }

.faq-item { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 16px 20px; margin-bottom: 12px; }
.faq-item h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin: 0 0 6px; }
.faq-item p { margin: 0; font-size: 13px; color: var(--color-gray-600); line-height: 1.5; }

.help-footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--color-gray-200); font-size: 11px; color: var(--color-gray-400); }
</style>
