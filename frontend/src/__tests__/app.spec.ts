import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from '../App.vue'

describe('App', () => {
  it('mounts successfully with RouterView', () => {
    const pinia = createPinia()
    const i18n = createI18n({ legacy: false, locale: 'fr', messages: { fr: {}, en: {} } })

    const wrapper = mount(App, {
      global: {
        plugins: [pinia, i18n],
        stubs: { RouterView: true },
      },
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'RouterView' }).exists()).toBe(true)
  })
})
