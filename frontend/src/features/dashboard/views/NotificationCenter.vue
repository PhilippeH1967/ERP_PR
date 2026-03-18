<script setup lang="ts">
import { ref } from 'vue'

interface NotificationItem {
  id: number
  notification_type: string
  message: string
  read_at: string | null
  created_at: string
}

const notifications = ref<NotificationItem[]>([])
// Will be fetched from /api/v1/notifications/ when endpoint is created
</script>

<template>
  <div>
    <h1 class="mb-6 text-2xl font-semibold text-text">
      Centre de notifications
    </h1>

    <div class="space-y-2">
      <div
        v-for="notif in notifications"
        :key="notif.id"
        class="flex items-center gap-3 rounded-lg border border-border bg-surface p-4"
        :class="{ 'border-primary/20 bg-primary/5': !notif.read_at }"
      >
        <div
          v-if="!notif.read_at"
          class="h-2 w-2 rounded-full bg-primary"
        />
        <div class="flex-1">
          <p class="text-sm text-text">
            {{ notif.message }}
          </p>
          <p class="text-xs text-text-muted">
            {{ notif.notification_type }} · {{ notif.created_at }}
          </p>
        </div>
      </div>

      <div
        v-if="!notifications.length"
        class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted"
      >
        Aucune notification
      </div>
    </div>
  </div>
</template>
