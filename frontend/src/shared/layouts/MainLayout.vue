<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/shared/composables/useAuth'
import { useLocale } from '@/shared/composables/useLocale'
import { useSidebarMenu } from '@/shared/composables/useSidebarMenu'
import { useSidebarBadges } from '@/shared/composables/useSidebarBadges'
import { useSidebarCollapse } from '@/shared/composables/useSidebarCollapse'
import apiClient from '@/plugins/axios'
import { useIdleTimeout } from '@/shared/composables/useIdleTimeout'
import CommandPalette from '@/shared/components/CommandPalette.vue'
import ActionCenterSection from '@/shared/components/ActionCenterSection.vue'

const { t } = useI18n()
const { currentUser, logout } = useAuth()
const { currentLocale, switchLocale, initLocale } = useLocale()
const { sections: sidebarSections, subtitleKey } = useSidebarMenu()
const { badges, health, hasNew } = useSidebarBadges()
const { isCollapsed, toggleSection } = useSidebarCollapse()
initLocale()

const userMenuOpen = ref(false)
const { showWarning: showIdleWarning, remainingSeconds, dismiss: dismissIdle } = useIdleTimeout(() => logout())
const unreadCount = ref(0)

interface ActiveDelegation {
  delegator_name: string
  scope: string
  project_id: number | null
}
const activeDelegation = ref<ActiveDelegation | null>(null)

async function fetchNotifCount() {
  try {
    const resp = await apiClient.get('notifications/')
    unreadCount.value = resp.data?.unread_count || 0
  } catch { unreadCount.value = 0 }
}

async function fetchDelegation() {
  try {
    const resp = await apiClient.get('delegations/')
    const delegations = resp.data?.data || []
    const today = new Date().toISOString().slice(0, 10)
    const userId = currentUser.value?.id
    const active = delegations.find(
      (d: { delegate: number; is_active: boolean; start_date: string; end_date: string }) =>
        d.delegate === userId && d.is_active && d.start_date <= today && d.end_date >= today,
    )
    activeDelegation.value = active
      ? { delegator_name: active.delegator_name, scope: active.scope, project_id: active.project_id }
      : null
  } catch { activeDelegation.value = null }
}

onMounted(() => {
  fetchNotifCount()
  fetchDelegation()
  setInterval(fetchNotifCount, 60000)
})

function toggleLocale() {
  switchLocale(currentLocale.value === 'fr' ? 'en' : 'fr')
}

// Sidebar is now driven by useSidebarMenu (role-adaptive matrix)
// See _bmad-output/tech-specs/tech-spec-sidebar-quick-win-2026-04-11.md
</script>

<template>
  <div class="flex h-screen" style="background: var(--color-gray-50);">
    <!-- Sidebar -->
    <aside
      class="flex flex-col border-r"
      style="width: 240px; min-width: 240px; background: var(--color-gray-100); border-color: var(--color-gray-200); min-height: 100vh;"
    >
      <!-- Logo area with contextual subtitle -->
      <div
        class="flex flex-col justify-center px-5"
        style="height: 56px; border-bottom: 1px solid var(--color-gray-200);"
      >
        <span style="font-size: 18px; font-weight: 800; color: var(--color-primary); letter-spacing: -0.5px; line-height: 1;">
          PR
          <span style="color: var(--color-gray-400); font-weight: 400;">| {{ t(subtitleKey) }}</span>
        </span>
        <span style="font-size: 9px; color: var(--color-gray-400); letter-spacing: 0.5px;">v1.2.000</span>
      </div>

      <!-- Action Center (Sprint 2 - B1) -->
      <ActionCenterSection />

      <!-- Navigation (role-adaptive + collapsible + badges) -->
      <nav class="flex-1 overflow-y-auto py-2">
        <template v-for="section in sidebarSections" :key="section.label">
          <div
            class="sidebar-section-header"
            @click="toggleSection(section.label)"
          >
            <span>{{ t(section.label) }}</span>
            <span class="collapse-arrow" :class="{ collapsed: isCollapsed(section.label) }">&#9662;</span>
          </div>
          <template v-if="!isCollapsed(section.label)">
            <router-link
              v-for="item in section.items"
              :key="`${section.label}-${item.key}`"
              :to="item.path"
              class="sidebar-item"
              active-class="sidebar-item-active"
            >
              <span style="width: 18px; text-align: center; font-size: 15px;">{{ item.icon }}</span>
              <span class="sidebar-item-label">{{ t(item.key) }}</span>
              <!-- Badge count (B4) -->
              <span
                v-if="(badges[item.path.replace('/', '')] ?? 0) > 0"
                class="sidebar-badge"
              >{{ badges[item.path.replace('/', '')] }}</span>
              <!-- Health dot (B5) -->
              <span
                v-if="health[item.path.replace('/', '')]"
                class="sidebar-health-dot"
                :class="`dot-${health[item.path.replace('/', '')]}`"
              ></span>
              <!-- Freshness dot (B4) -->
              <span
                v-if="hasNew[item.path.replace('/', '')]"
                class="sidebar-new-dot"
              ></span>
            </router-link>
          </template>
        </template>
      </nav>
    </aside>

    <!-- Main content area -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Top bar -->
      <header
        class="flex items-center justify-between px-6"
        style="height: 56px; background: white; border-bottom: 1px solid var(--color-gray-200);"
      >
        <!-- Search -->
        <div class="flex items-center">
          <input
            type="text"
            :placeholder="t('nav.search')"
            class="topbar-search"
          >
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-4">
          <!-- Locale toggle -->
          <button
            class="rounded px-2 py-1 text-xs font-medium"
            style="color: var(--color-gray-500);"
            @click="toggleLocale"
          >
            {{ currentLocale === 'fr' ? 'EN' : 'FR' }}
          </button>

          <!-- Notifications bell -->
          <router-link to="/notifications" class="topbar-bell">
            <span>🔔</span>
            <span v-if="unreadCount > 0" class="bell-badge">{{ unreadCount }}</span>
          </router-link>

          <!-- User avatar + menu -->
          <div class="relative">
            <button
              class="topbar-avatar"
              @click="userMenuOpen = !userMenuOpen"
            >
              {{ currentUser?.email?.substring(0, 2).toUpperCase() || 'U' }}
            </button>
            <div
              v-if="userMenuOpen"
              class="absolute right-0 top-full z-50 mt-1 w-56 rounded-lg border bg-white py-1"
              style="border-color: var(--color-gray-200); box-shadow: var(--shadow-lg);"
            >
              <div class="px-4 py-2 border-b" style="border-color: var(--color-gray-100);">
                <p class="text-sm font-medium" style="color: var(--color-gray-800);">
                  {{ currentUser?.email || t('nav.user') }}
                </p>
                <p class="text-xs" style="color: var(--color-gray-500);">
                  {{ currentUser?.roles?.join(', ') }}
                </p>
              </div>
              <button
                class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50"
                style="color: var(--color-gray-600);"
                @click="logout(); userMenuOpen = false"
              >
                {{ t('auth.logout') }}
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Idle timeout warning (FR77) -->
      <div v-if="showIdleWarning" class="idle-warning">
        <span>Votre session expire dans <strong>{{ remainingSeconds }}s</strong> — bougez la souris pour rester connecté.</span>
        <button @click="dismissIdle" class="idle-dismiss">Rester connecté</button>
      </div>

      <!-- Delegation banner -->
      <div v-if="activeDelegation" class="delegation-banner">
        <span>Par délégation de <strong>{{ activeDelegation.delegator_name }}</strong></span>
        <span class="delegation-scope">{{ activeDelegation.scope === 'all' ? 'Tous projets' : `Projet #${activeDelegation.project_id}` }}</span>
        <router-link to="/delegations" class="delegation-link">Voir délégations</router-link>
      </div>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>

    <!-- Cmd+K search (Sprint 2 - B3) -->
    <CommandPalette />
  </div>
</template>

<style scoped>
.sidebar-item {
  padding: 9px 20px 9px 28px;
  font-size: 14px;
  color: var(--color-gray-600);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.15s;
  text-decoration: none;
}
.sidebar-item:hover {
  background: var(--color-gray-200);
  color: var(--color-gray-800);
}
.sidebar-item-active {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 600;
}

/* Sprint 2 — Collapsible sections */
.sidebar-section-header {
  padding: 10px 20px 4px;
  font-size: 10px;
  font-weight: 700;
  color: var(--color-gray-400);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
}
.sidebar-section-header:hover {
  color: var(--color-gray-600);
}
.collapse-arrow {
  font-size: 10px;
  transition: transform 0.15s;
}
.collapse-arrow.collapsed {
  transform: rotate(-90deg);
}
.sidebar-item-label {
  flex: 1;
}

/* Sprint 2 — Badges */
.sidebar-badge {
  font-size: 10px;
  font-weight: 700;
  color: white;
  background: var(--color-danger, #DC2626);
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
}

/* Sprint 2 — Health dots */
.sidebar-health-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-green { background: #16A34A; }
.dot-amber { background: #D97706; }
.dot-red { background: #DC2626; }

/* Sprint 2 — Freshness dot */
.sidebar-new-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #2563EB;
  flex-shrink: 0;
}

.topbar-search {
  padding: 8px 12px 8px 36px;
  border: 1px solid var(--color-gray-200);
  border-radius: 8px;
  font-size: 13px;
  width: 280px;
  background: var(--color-gray-50) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%239CA3AF' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85zm-5.242.656a5 5 0 1 1 0-10 5 5 0 0 1 0 10z'/%3E%3C/svg%3E") no-repeat 12px center;
}
.topbar-search:focus {
  outline: none;
  border-color: var(--color-primary);
}

.topbar-bell {
  position: relative;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-gray-50);
  border: 1px solid var(--color-gray-200);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
}
.bell-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--color-danger);
  color: white;
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.idle-warning {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 24px;
  background: #FEE2E2;
  border-bottom: 1px solid #FECACA;
  font-size: 12px;
  color: #DC2626;
}
.idle-dismiss {
  background: white;
  border: 1px solid #DC2626;
  color: #DC2626;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}
.idle-dismiss:hover {
  background: #FEE2E2;
}

.delegation-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 24px;
  background: #FEF3C7;
  border-bottom: 1px solid #FCD34D;
  font-size: 12px;
  color: #92400E;
}
.delegation-scope {
  padding: 1px 8px;
  border-radius: 10px;
  background: rgba(146, 64, 14, 0.1);
  font-weight: 600;
  font-size: 10px;
}
.delegation-link {
  margin-left: auto;
  color: #1D4ED8;
  font-weight: 600;
  text-decoration: none;
}
.delegation-link:hover {
  text-decoration: underline;
}

.topbar-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  border: none;
}
</style>
