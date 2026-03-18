import { createRouter, createWebHistory } from 'vue-router'
import { authGuard } from './guards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/shared/layouts/AuthLayout.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/shared/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        {
          path: 'timesheets',
          name: 'timesheets',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        {
          path: 'projects',
          name: 'projects',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        {
          path: 'billing',
          name: 'billing',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        {
          path: 'expenses',
          name: 'expenses',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(authGuard)

export default router
