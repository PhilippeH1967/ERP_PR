<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-surface-alt">
    <div class="text-center">
      <h1 class="text-2xl font-semibold text-primary">
        {{ t('app.name') }}
      </h1>
      <p class="mt-2 text-text-muted">
        Platform ready
      </p>
    </div>
  </div>
</template>
