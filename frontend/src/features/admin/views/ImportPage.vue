<script setup lang="ts">
import { onMounted, ref } from 'vue'
import apiClient from '@/plugins/axios'

interface ImportType {
  key: string
  label: string
  description: string
  file: string
  order: number
  icon: string
}

const importTypes = ref<ImportType[]>([])
const uploadStatus = ref<Record<string, { loading: boolean; message: string; error: boolean }>>({})

onMounted(async () => {
  try {
    const resp = await apiClient.get('imports/')
    const data = resp.data?.data || resp.data
    importTypes.value = data?.import_types || []
  } catch {
    importTypes.value = []
  }
})

function downloadTemplate(key: string, _filename: string) {
  window.open(`/api/v1/imports/${key}/template/`, '_blank')
}

async function uploadFile(key: string, event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploadStatus.value[key] = { loading: true, message: 'Import en cours...', error: false }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const resp = await apiClient.post(`imports/${key}/upload/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const data = resp.data?.data || resp.data
    uploadStatus.value[key] = {
      loading: false,
      message: data?.output || 'Import réussi!',
      error: false,
    }
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: { message?: string } } } }
    uploadStatus.value[key] = {
      loading: false,
      message: axiosErr.response?.data?.error?.message || 'Erreur lors de l\'import',
      error: true,
    }
  }

  input.value = ''
}
</script>

<template>
  <div>
    <h1 class="mb-2 text-2xl font-semibold text-text">
      Import de données
    </h1>
    <p class="mb-6 text-sm text-text-muted">
      Importez vos données ChangePoint via des fichiers Excel.
      Téléchargez le template, remplissez-le, puis uploadez-le.
    </p>

    <!-- Import order notice -->
    <div class="mb-6 rounded-lg border border-primary/20 bg-primary/5 p-4">
      <h3 class="text-sm font-medium text-primary">
        Ordre d'import recommandé
      </h3>
      <p class="mt-1 text-xs text-text-muted">
        1. Employés → 2. Clients → 3. Sous-traitants → 4. Projets → 5. Feuilles de temps
      </p>
    </div>

    <!-- Import cards -->
    <div class="space-y-4">
      <div
        v-for="imp in importTypes"
        :key="imp.key"
        class="rounded-lg border border-border bg-surface p-6"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start gap-4">
            <span class="text-3xl">{{ imp.icon }}</span>
            <div>
              <h3 class="text-sm font-semibold text-text">
                {{ imp.order }}. {{ imp.label }}
              </h3>
              <p class="mt-0.5 text-xs text-text-muted">
                {{ imp.description }}
              </p>
            </div>
          </div>

          <div class="flex gap-2">
            <!-- Download template -->
            <button
              class="rounded-md border border-border bg-surface px-4 py-2 text-xs font-medium text-text-muted hover:bg-surface-alt"
              @click="downloadTemplate(imp.key, imp.file)"
            >
              📥 Télécharger template
            </button>

            <!-- Upload -->
            <label
              class="cursor-pointer rounded-md bg-primary px-4 py-2 text-xs font-medium text-white hover:bg-primary-light"
            >
              📤 Importer fichier
              <input
                type="file"
                accept=".xlsx,.xls"
                class="hidden"
                @change="(e) => uploadFile(imp.key, e)"
              >
            </label>
          </div>
        </div>

        <!-- Status feedback -->
        <div
          v-if="uploadStatus[imp.key]"
          class="mt-3 rounded p-3 text-xs"
          :class="uploadStatus[imp.key].error
            ? 'bg-danger/10 text-danger'
            : uploadStatus[imp.key].loading
              ? 'bg-primary/10 text-primary'
              : 'bg-success/10 text-success'"
        >
          <pre class="whitespace-pre-wrap font-mono">{{ uploadStatus[imp.key].message }}</pre>
        </div>
      </div>
    </div>

    <!-- Seed reference data note -->
    <div class="mt-8 rounded-lg border border-warning/20 bg-warning/5 p-4">
      <h3 class="text-sm font-medium text-warning">
        Données de référence
      </h3>
      <p class="mt-1 text-xs text-text-muted">
        Les catégories de dépenses, templates de projet et niveaux de relance
        sont créés automatiquement lors du premier import.
        Pour les réinitialiser, exécutez :
      </p>
      <code class="mt-2 block rounded bg-surface-alt p-2 text-xs font-mono">
        python manage.py seed_reference_data --tenant=provencher-roy
      </code>
    </div>
  </div>
</template>
