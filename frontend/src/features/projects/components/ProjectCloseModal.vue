<script setup lang="ts">
interface Check {
  code: string
  label: string
  passed: boolean
  detail: string
  severity?: string
}

defineProps<{
  open: boolean
  canClose: boolean
  checks: Check[]
  loading?: boolean
  errorMessage?: string
}>()

const emit = defineEmits<{
  close: []
  confirm: []
}>()
</script>

<template>
  <div v-if="open" class="cm-overlay" @click.self="emit('close')">
    <div class="cm-panel" role="dialog" aria-modal="true">
      <header class="cm-header">
        <h3 class="cm-title">Clôturer le projet</h3>
        <button class="cm-close" aria-label="Fermer" @click="emit('close')">×</button>
      </header>

      <div class="cm-body">
        <p class="cm-intro">
          Avant de passer le projet en <strong>Terminé</strong>, vérifiez que tous
          les prérequis sont remplis. Les avertissements (⚠) n'empêchent pas la clôture
          mais méritent votre attention.
        </p>

        <ul class="cm-list">
          <li
            v-for="c in checks"
            :key="c.code"
            data-check-row
            :data-passed="String(c.passed)"
            :data-severity="c.severity || 'blocker'"
            class="cm-row"
            :class="{
              'cm-row-ok': c.passed,
              'cm-row-warn': !c.passed && c.severity === 'warning',
              'cm-row-err': !c.passed && c.severity !== 'warning',
            }"
          >
            <span class="cm-icon">
              <template v-if="c.passed">✓</template>
              <template v-else-if="c.severity === 'warning'">⚠</template>
              <template v-else>✗</template>
            </span>
            <div class="cm-content">
              <div class="cm-label">{{ c.label }}</div>
              <div class="cm-detail">{{ c.detail }}</div>
            </div>
          </li>
        </ul>

        <div v-if="errorMessage" class="cm-error">{{ errorMessage }}</div>
      </div>

      <footer class="cm-footer">
        <button data-close-cancel class="cm-btn" :disabled="loading" @click="emit('close')">
          Annuler
        </button>
        <button
          data-close-confirm
          class="cm-btn cm-btn-primary"
          :disabled="!canClose || loading"
          @click="emit('confirm')"
        >
          {{ loading ? 'Clôture…' : 'Clôturer le projet' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.cm-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.cm-panel { background: white; border-radius: 8px; max-width: 560px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); }
.cm-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--color-gray-200); }
.cm-title { font-size: 16px; font-weight: 700; color: var(--color-gray-800); margin: 0; }
.cm-close { background: none; border: none; font-size: 22px; color: var(--color-gray-500); cursor: pointer; line-height: 1; }
.cm-close:hover { color: var(--color-gray-800); }
.cm-body { padding: 18px; overflow-y: auto; }
.cm-intro { font-size: 13px; color: var(--color-gray-600); margin: 0 0 16px; line-height: 1.5; }
.cm-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.cm-row { display: flex; align-items: flex-start; gap: 12px; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--color-gray-200); background: white; }
.cm-row-ok { border-color: #bbf7d0; background: #f0fdf4; }
.cm-row-warn { border-color: #fde68a; background: #fffbeb; }
.cm-row-err { border-color: #fecaca; background: #fef2f2; }
.cm-icon { font-size: 18px; font-weight: 700; line-height: 1.2; min-width: 20px; }
.cm-row-ok .cm-icon { color: #16a34a; }
.cm-row-warn .cm-icon { color: #d97706; }
.cm-row-err .cm-icon { color: #dc2626; }
.cm-content { flex: 1; }
.cm-label { font-size: 13px; font-weight: 600; color: var(--color-gray-800); }
.cm-detail { font-size: 12px; color: var(--color-gray-600); margin-top: 2px; }
.cm-error { margin-top: 12px; padding: 8px 12px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 4px; color: #b91c1c; font-size: 12px; }
.cm-footer { display: flex; justify-content: flex-end; gap: 8px; padding: 12px 18px; border-top: 1px solid var(--color-gray-200); background: var(--color-gray-50); border-radius: 0 0 8px 8px; }
.cm-btn { padding: 8px 14px; border: 1px solid var(--color-gray-300); background: white; border-radius: 4px; font-size: 13px; font-weight: 600; color: var(--color-gray-700); cursor: pointer; }
.cm-btn:hover:not(:disabled) { background: var(--color-gray-100); }
.cm-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.cm-btn-primary { background: var(--color-primary); border-color: var(--color-primary); color: white; }
.cm-btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
</style>
