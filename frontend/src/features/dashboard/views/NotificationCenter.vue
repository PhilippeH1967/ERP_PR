<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import apiClient from '@/plugins/axios'
import { useLocale } from '@/shared/composables/useLocale'

const { fmt } = useLocale()

interface NotificationItem {
  id: number
  type: string
  message: string
  read: boolean
  created_at: string
}

const notifications = ref<NotificationItem[]>([])
const unreadCount = ref(0)
const filter = ref<'all' | 'unread'>('all')

const filtered = computed(() => {
  if (filter.value === 'unread') return notifications.value.filter(n => !n.read)
  return notifications.value
})

async function fetch() {
  try {
    const resp = await apiClient.get('notifications/')
    const data = resp.data
    notifications.value = data?.data || []
    unreadCount.value = data?.unread_count || 0
  } catch { notifications.value = [] }
}

async function markRead(id: number) {
  await apiClient.post(`notifications/${id}/read/`)
  const notif = notifications.value.find(n => n.id === id)
  if (notif) { notif.read = true; unreadCount.value = Math.max(0, unreadCount.value - 1) }
}

async function markAllRead() {
  await apiClient.post('notifications/read-all/')
  notifications.value.forEach(n => { n.read = true })
  unreadCount.value = 0
}

const typeIcons: Record<string, string> = {
  timesheet: '🕐',
  invoice: '📄',
  expense: '🧾',
  project: '📁',
  approval: '✅',
  system: '⚙️',
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>
        Centre de notifications
        <span v-if="unreadCount" class="unread-badge">{{ unreadCount }}</span>
      </h1>
      <div class="header-actions">
        <div class="filter-tabs">
          <button :class="{ active: filter === 'all' }" @click="filter = 'all'">Toutes</button>
          <button :class="{ active: filter === 'unread' }" @click="filter = 'unread'">Non lues</button>
        </div>
        <button v-if="unreadCount" class="btn-ghost" @click="markAllRead">Tout marquer lu</button>
      </div>
    </div>

    <div class="notif-list">
      <div
        v-for="notif in filtered"
        :key="notif.id"
        class="notif-item"
        :class="{ unread: !notif.read }"
        @click="!notif.read && markRead(notif.id)"
      >
        <span class="notif-icon">{{ typeIcons[notif.type] || '🔔' }}</span>
        <div class="notif-content">
          <p class="notif-message">{{ notif.message }}</p>
          <p class="notif-meta">
            <span class="notif-type">{{ notif.type }}</span>
            · {{ fmt.dateTime(notif.created_at) }}
          </p>
        </div>
        <div v-if="!notif.read" class="notif-dot" />
      </div>

      <div v-if="!filtered.length" class="empty">
        {{ filter === 'unread' ? 'Aucune notification non lue' : 'Aucune notification' }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); display: flex; align-items: center; gap: 8px; }
.unread-badge { font-size: 11px; font-weight: 700; background: var(--color-danger); color: white; padding: 1px 7px; border-radius: 10px; }
.header-actions { display: flex; align-items: center; gap: 10px; }
.filter-tabs { display: flex; gap: 0; border: 1px solid var(--color-gray-200); border-radius: 6px; overflow: hidden; }
.filter-tabs button { padding: 4px 12px; font-size: 11px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: white; }
.filter-tabs button.active { background: var(--color-primary); color: white; }

.notif-list { display: flex; flex-direction: column; gap: 6px; }
.notif-item { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); cursor: pointer; transition: all 0.15s; border: 1px solid transparent; }
.notif-item.unread { border-color: var(--color-primary); background: rgba(37,99,235,0.03); }
.notif-item:hover { box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
.notif-icon { font-size: 18px; flex-shrink: 0; margin-top: 2px; }
.notif-content { flex: 1; min-width: 0; }
.notif-message { font-size: 13px; color: var(--color-gray-800); line-height: 1.4; }
.notif-meta { font-size: 11px; color: var(--color-gray-500); margin-top: 2px; }
.notif-type { font-weight: 600; text-transform: capitalize; }
.notif-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-primary); flex-shrink: 0; margin-top: 6px; }
.empty { text-align: center; padding: 40px; color: var(--color-gray-400); background: white; border-radius: 8px; font-size: 13px; }
</style>
