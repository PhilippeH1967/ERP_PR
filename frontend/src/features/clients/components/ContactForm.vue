<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [data: { name: string; role: string; email: string; phone: string; language_preference: string }]
  cancel: []
}>()

const form = ref({
  name: '',
  role: '',
  email: '',
  phone: '',
  language_preference: 'fr',
})

const error = ref('')

function validateEmail(email: string): boolean {
  if (!email) return true // optional
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function onSubmit() {
  error.value = ''
  if (!form.value.name.trim()) {
    error.value = 'Le nom est obligatoire.'
    return
  }
  if (form.value.email && !validateEmail(form.value.email)) {
    error.value = 'Le format du courriel est invalide.'
    return
  }
  emit('submit', { ...form.value })
  form.value = { name: '', role: '', email: '', phone: '', language_preference: 'fr' }
}
</script>

<template>
  <div class="rounded-lg border border-primary/20 bg-primary/5 p-4">
    <h4 class="mb-3 text-sm font-medium text-primary">Nouveau contact</h4>

    <div v-if="error" class="mb-3 rounded bg-danger/10 p-2 text-xs text-danger">{{ error }}</div>

    <div class="grid grid-cols-2 gap-3">
      <div>
        <input v-model="form.name" type="text" placeholder="Nom *"
          class="w-full rounded border px-2 py-1.5 text-sm"
          :class="error && !form.name.trim() ? 'border-danger' : 'border-border'" />
      </div>
      <input v-model="form.role" type="text" placeholder="Rôle"
        class="rounded border border-border px-2 py-1.5 text-sm" />
      <div>
        <input v-model="form.email" type="email" placeholder="Courriel"
          class="w-full rounded border px-2 py-1.5 text-sm"
          :class="error && form.email && !validateEmail(form.email) ? 'border-danger' : 'border-border'" />
      </div>
      <input v-model="form.phone" type="text" placeholder="Téléphone"
        class="rounded border border-border px-2 py-1.5 text-sm" />
      <select v-model="form.language_preference"
        class="rounded border border-border px-2 py-1.5 text-sm">
        <option value="fr">Français</option>
        <option value="en">English</option>
      </select>
    </div>
    <div class="mt-3 flex gap-2">
      <button class="rounded bg-primary px-3 py-1.5 text-xs font-medium text-white" @click="onSubmit">Ajouter</button>
      <button class="rounded px-3 py-1.5 text-xs text-text-muted hover:bg-surface-alt" @click="emit('cancel')">Annuler</button>
    </div>
  </div>
</template>
