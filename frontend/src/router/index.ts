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
        { path: '', name: 'home', redirect: '/dashboard' },
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
        {
          path: 'projects/new',
          name: 'project-create',
          component: () => import('@/features/projects/views/ProjectCreate.vue'),
        },
        {
          path: 'projects/:id',
          name: 'project-detail',
          component: () => import('@/features/projects/views/ProjectDetail.vue'),
        },
        // Timesheets
        {
          path: 'timesheets',
          name: 'timesheets',
          component: () => import('@/features/timesheet/views/TimesheetGrid.vue'),
        },
        {
          path: 'approvals',
          name: 'approvals',
          component: () => import('@/features/timesheet/views/ApprovalQueue.vue'),
        },
        // Billing
        {
          path: 'billing',
          name: 'billing',
          component: () => import('@/features/billing/views/InvoiceList.vue'),
        },
        // Expenses
        {
          path: 'expenses',
          name: 'expenses',
          component: () => import('@/features/expenses/views/ExpenseList.vue'),
        },
        // Suppliers
        {
          path: 'suppliers',
          name: 'suppliers',
          component: () => import('@/features/suppliers/views/SupplierList.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(authGuard)

export default router
