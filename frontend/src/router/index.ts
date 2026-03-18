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
          redirect: '/dashboard',
        },
        // Dashboard
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/features/dashboard/views/DashboardView.vue'),
        },
        // Clients
        {
          path: 'clients',
          name: 'clients',
          component: () => import('@/features/clients/views/ClientList.vue'),
        },
        {
          path: 'clients/:id',
          name: 'client-detail',
          component: () => import('@/features/clients/views/ClientDetail.vue'),
        },
        // Projects
        {
          path: 'projects',
          name: 'projects',
          component: () => import('@/features/projects/views/ProjectList.vue'),
        },
        // Timesheets
        {
          path: 'timesheets',
          name: 'timesheets',
          component: () => import('@/features/timesheet/views/TimesheetGrid.vue'),
        },
        // Billing
        {
          path: 'billing',
          name: 'billing',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        // Expenses
        {
          path: 'expenses',
          name: 'expenses',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
        // Suppliers
        {
          path: 'suppliers',
          name: 'suppliers',
          component: () => import('@/shared/layouts/HomeView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(authGuard)

export default router
