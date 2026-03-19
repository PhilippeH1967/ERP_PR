<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useAuth } from '@/shared/composables/useAuth'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const { t } = useI18n()
const router = useRouter()
const { loginWithCredentials, loginSSO, fetchAuthConfig, authConfig } = useAuth()

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const isLoading = ref(false)

onMounted(async () => {
  await fetchAuthConfig()
})

async function handleLocalLogin() {
  if (!username.value || !password.value) return
  isLoading.value = true
  error.value = null
  try {
    await loginWithCredentials(username.value, password.value)
    const redirect = (router.currentRoute.value.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e: unknown) {
    const axiosError = e as { response?: { data?: { detail?: string } } }
    if (axiosError.response?.data?.detail) {
      error.value = axiosError.response.data.detail
    } else {
      error.value = t('auth.login_error')
    }
  } finally {
    isLoading.value = false
  }
}

async function handleSSOLogin() {
  isLoading.value = true
  error.value = null
  try {
    await loginSSO()
  } catch {
    error.value = t('auth.sso_unavailable')
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Logo -->
      <div class="login-logo">
        <span class="logo-pr">PR</span>
        <span class="logo-sep">|</span>
        <span class="logo-erp">ERP</span>
      </div>
      <p class="login-subtitle">Services Professionnels</p>
      <p class="login-version">v1.1.004</p>

      <!-- Error -->
      <div v-if="error" class="login-error">
        {{ error }}
      </div>

      <!-- Local login form -->
      <form @submit.prevent="handleLocalLogin" class="login-form">
        <div class="form-group">
          <label for="username">{{ t('auth.username') }}</label>
          <input
            id="username"
            v-model="username"
            type="text"
            autocomplete="username"
            :placeholder="t('auth.username_placeholder')"
          />
        </div>

        <div class="form-group">
          <label for="password">{{ t('auth.password') }}</label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            :placeholder="t('auth.password_placeholder')"
          />
        </div>

        <button
          type="submit"
          class="btn-login"
          :disabled="isLoading || !username || !password"
        >
          {{ isLoading ? t('app.loading') : t('auth.login') }}
        </button>
      </form>

      <!-- SSO (shown only when configured) -->
      <template v-if="authConfig.sso_available">
        <div class="login-divider">
          <span>{{ t('auth.or') }}</span>
        </div>

        <button
          class="btn-sso"
          :disabled="isLoading"
          @click="handleSSOLogin"
        >
          {{ t('auth.login_sso') }}
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-gray-50);
}
.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
  padding: 40px 32px;
}
.login-logo {
  text-align: center;
  margin-bottom: 4px;
}
.logo-pr {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-primary);
  letter-spacing: -0.5px;
}
.logo-sep {
  font-size: 28px;
  font-weight: 300;
  color: var(--color-gray-300);
  margin: 0 6px;
}
.logo-erp {
  font-size: 28px;
  font-weight: 400;
  color: var(--color-gray-400);
}
.login-subtitle {
  text-align: center;
  font-size: 13px;
  color: var(--color-gray-500);
  margin-bottom: 4px;
}
.login-version {
  text-align: center;
  font-size: 9px;
  color: var(--color-gray-400);
  letter-spacing: 0.5px;
  margin-bottom: 28px;
}
.login-error {
  background: var(--color-danger-light);
  color: var(--color-danger);
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  margin-bottom: 16px;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-gray-700);
  margin-bottom: 6px;
}
.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-gray-300);
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  background: white;
}
.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
.btn-login {
  width: 100%;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background: var(--color-primary);
  color: white;
  transition: all 0.15s;
}
.btn-login:hover:not(:disabled) {
  background: var(--color-primary-dark);
}
.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.login-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 24px 0;
}
.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  border-top: 1px solid var(--color-gray-200);
}
.login-divider span {
  font-size: 12px;
  color: var(--color-gray-400);
}
.btn-sso {
  width: 100%;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  background: white;
  color: var(--color-gray-600);
  border: 1px solid var(--color-gray-300);
  transition: all 0.15s;
}
.btn-sso:hover:not(:disabled) {
  background: var(--color-gray-100);
}
.btn-sso:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
