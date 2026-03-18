<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/shared/composables/useAuth'
import { ref } from 'vue'

const { t } = useI18n()
const { login } = useAuth()
const error = ref<string | null>(null)
const isLoading = ref(false)

async function handleLogin() {
  isLoading.value = true
  error.value = null
  try {
    await login()
  } catch {
    error.value = t('auth.sso_unavailable')
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-surface-alt">
    <div class="w-full max-w-sm rounded-lg bg-surface p-8 shadow-lg">
      <div class="mb-8 text-center">
        <h1 class="text-2xl font-semibold text-primary">
          {{ t('app.name') }}
        </h1>
      </div>

      <div
        v-if="error"
        class="mb-4 rounded-md bg-danger/10 p-3 text-sm text-danger"
      >
        {{ error }}
      </div>

      <button
        class="w-full rounded-md bg-primary px-4 py-3 font-medium text-white transition-colors hover:bg-primary-light disabled:opacity-50"
        :disabled="isLoading"
        @click="handleLogin"
      >
        {{ isLoading ? t('app.loading') : t('auth.login') }}
      </button>
    </div>
  </div>
</template>
