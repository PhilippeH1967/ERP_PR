/**
 * Idle timeout composable (FR77 — 30min inactivity timeout).
 *
 * Tracks user activity (mouse, keyboard, touch, scroll).
 * Shows warning at 25min, auto-logout at 30min.
 */

import { ref, onMounted, onUnmounted } from 'vue'

const TIMEOUT_MS = 30 * 60 * 1000 // 30 minutes
const WARNING_MS = 25 * 60 * 1000 // 25 minutes (warn 5min before)

export function useIdleTimeout(onLogout: () => void) {
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let warningId: ReturnType<typeof setTimeout> | null = null

  const showWarning = ref(false)
  const remainingSeconds = ref(0)
  let countdownInterval: ReturnType<typeof setInterval> | null = null

  const ACTIVITY_EVENTS = ['mousemove', 'mousedown', 'keydown', 'touchstart', 'scroll']

  function resetTimer() {
    showWarning.value = false
    remainingSeconds.value = 0

    if (timeoutId) clearTimeout(timeoutId)
    if (warningId) clearTimeout(warningId)
    if (countdownInterval) clearInterval(countdownInterval)

    // Warning at 25min
    warningId = setTimeout(() => {
      showWarning.value = true
      remainingSeconds.value = Math.round((TIMEOUT_MS - WARNING_MS) / 1000)
      countdownInterval = setInterval(() => {
        remainingSeconds.value--
        if (remainingSeconds.value <= 0 && countdownInterval) {
          clearInterval(countdownInterval)
        }
      }, 1000)
    }, WARNING_MS)

    // Logout at 30min
    timeoutId = setTimeout(() => {
      showWarning.value = false
      if (countdownInterval) clearInterval(countdownInterval)
      onLogout()
    }, TIMEOUT_MS)
  }

  function dismiss() {
    resetTimer()
  }

  onMounted(() => {
    resetTimer()
    ACTIVITY_EVENTS.forEach(event => {
      document.addEventListener(event, resetTimer, { passive: true })
    })
  })

  onUnmounted(() => {
    if (timeoutId) clearTimeout(timeoutId)
    if (warningId) clearTimeout(warningId)
    if (countdownInterval) clearInterval(countdownInterval)
    ACTIVITY_EVENTS.forEach(event => {
      document.removeEventListener(event, resetTimer)
    })
  })

  return { showWarning, remainingSeconds, dismiss }
}
