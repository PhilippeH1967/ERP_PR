<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/shared/composables/useAuth'
import { useLocale } from '@/shared/composables/useLocale'

const { t } = useI18n()
const { currentUser, logout } = useAuth()
const { currentLocale, switchLocale } = useLocale()

const sidebarCollapsed = ref(false)
const userMenuOpen = ref(false)

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

function toggleLocale() {
  switchLocale(currentLocale.value === 'fr' ? 'en' : 'fr')
}

const navItems = [
  { name: 'nav.dashboard', path: '/dashboard', icon: 'chart-bar' },
  { name: 'nav.timesheets', path: '/timesheets', icon: 'clock' },
  { name: 'nav.projects', path: '/projects', icon: 'folder' },
  { name: 'nav.billing', path: '/billing', icon: 'document-text' },
  { name: 'nav.expenses', path: '/expenses', icon: 'receipt' },
  { name: 'nav.suppliers', path: '/suppliers', icon: 'building' },
]
</script>

<template>
  <div class="flex h-screen bg-surface-alt">
    <!-- Sidebar -->
    <aside
      class="flex flex-col border-r border-border bg-surface transition-all duration-200"
      :class="sidebarCollapsed ? 'w-16' : 'w-60'"
    >
      <!-- Logo -->
      <div class="flex h-14 items-center border-b border-border px-4">
        <span
          v-if="!sidebarCollapsed"
          class="text-lg font-semibold text-primary"
        >
          ERP
        </span>
        <span
          v-else
          class="mx-auto text-lg font-semibold text-primary"
        >
          E
        </span>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto p-2">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="mb-1 flex items-center rounded-md px-3 py-2 text-sm text-text-muted transition-colors hover:bg-surface-alt hover:text-text"
          active-class="bg-primary/10 text-primary font-medium"
        >
          <span
            v-if="!sidebarCollapsed"
            class="ml-2"
          >
            {{ t(item.name) }}
          </span>
        </router-link>
      </nav>

      <!-- Collapse toggle -->
      <button
        class="flex h-10 items-center justify-center border-t border-border text-text-muted hover:text-text"
        @click="toggleSidebar"
      >
        {{ sidebarCollapsed ? '&raquo;' : '&laquo;' }}
      </button>
    </aside>

    <!-- Main content area -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Top bar -->
      <header class="flex h-14 items-center justify-between border-b border-border bg-surface px-6">
        <!-- Search -->
        <div class="flex items-center">
          <input
            type="text"
            :placeholder="t('nav.search')"
            class="w-64 rounded-md border border-border bg-surface-alt px-3 py-1.5 text-sm focus:border-primary focus:outline-none"
          />
        </div>

        <!-- Right side: locale, notifications, user menu -->
        <div class="flex items-center gap-4">
          <!-- Locale toggle -->
          <button
            class="rounded-md px-2 py-1 text-xs font-medium text-text-muted hover:bg-surface-alt"
            @click="toggleLocale"
          >
            {{ currentLocale === 'fr' ? 'EN' : 'FR' }}
          </button>

          <!-- Notifications bell -->
          <button class="relative text-text-muted hover:text-text">
            <span class="text-lg">&#128276;</span>
          </button>

          <!-- User menu -->
          <div class="relative">
            <button
              class="flex items-center gap-2 text-sm text-text-muted hover:text-text"
              @click="userMenuOpen = !userMenuOpen"
            >
              <span>{{ currentUser?.email || t('nav.user') }}</span>
            </button>
            <div
              v-if="userMenuOpen"
              class="absolute right-0 top-full z-50 mt-1 w-48 rounded-md border border-border bg-surface py-1 shadow-lg"
            >
              <button
                class="w-full px-4 py-2 text-left text-sm text-text-muted hover:bg-surface-alt"
                @click="logout(); userMenuOpen = false"
              >
                {{ t('auth.logout') }}
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>
