<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

interface FavoriteItem {
  key: string
  label: string
  path: string
  icon: string
}

const emit = defineEmits<{
  'toggle-favorite': [key: string]
}>()

const router = useRouter()
const favorites = ref<FavoriteItem[]>([])

async function fetchConfig() {
  try {
    const resp = await apiClient.get('sidebar/config/')
    const data = resp.data?.data ?? resp.data
    favorites.value = data?.favorites ?? []
  } catch {
    favorites.value = []
  }
}

function navigateTo(path: string) {
  router.push(path)
}

function onToggleFavorite(key: string, event: Event) {
  event.stopPropagation()
  emit('toggle-favorite', key)
  // Optimistic removal from local list
  favorites.value = favorites.value.filter((f) => f.key !== key)
}

onMounted(fetchConfig)
</script>

<template>
  <div
    v-if="favorites.length > 0"
    class="sidebar-favorites"
  >
    <a
      v-for="fav in favorites"
      :key="fav.key"
      class="sidebar-favorite-item"
      @click="navigateTo(fav.path)"
    >
      <span class="sidebar-favorite-icon">{{ fav.icon }}</span>
      <span class="sidebar-favorite-label">{{ fav.label }}</span>
      <button
        class="sidebar-favorite-star"
        title="Retirer des favoris"
        @click="onToggleFavorite(fav.key, $event)"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          class="w-3.5 h-3.5"
        >
          <path
            fill-rule="evenodd"
            d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </a>
  </div>
</template>

<style scoped>
.sidebar-favorites {
  padding: 4px 0;
}

.sidebar-favorite-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 16px;
  cursor: pointer;
  transition: background-color 0.1s;
}

.sidebar-favorite-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.sidebar-favorite-icon {
  font-size: 14px;
  flex-shrink: 0;
}

.sidebar-favorite-label {
  flex: 1;
  font-size: 13px;
  color: #cdd6f4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-favorite-star {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #f9e2af;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.15s;
  padding: 2px;
  flex-shrink: 0;
}

.sidebar-favorite-item:hover .sidebar-favorite-star {
  opacity: 1;
}

.sidebar-favorite-star:hover {
  color: #fab387;
}
</style>
