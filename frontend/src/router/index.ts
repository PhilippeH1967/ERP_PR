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
        {
          path: 'notifications',
          name: 'notifications',
          component: () => import('@/features/dashboard/views/NotificationCenter.vue'),
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
        {
          path: 'billing/:id',
          name: 'invoice-detail',
          component: () => import('@/features/billing/views/InvoiceDetail.vue'),
        },
        {
          path: 'payments',
          name: 'payments',
          component: () => import('@/features/billing/views/PaymentList.vue'),
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
        {
          path: 'st-invoices',
          name: 'st-invoices',
          component: () => import('@/features/suppliers/views/STInvoiceList.vue'),
        },
        // Delegation
        {
          path: 'delegations',
          name: 'delegations',
          component: () => import('@/features/delegation/views/DelegationList.vue'),
        },
        // Admin
        {
          path: 'admin',
          name: 'admin',
          component: () => import('@/features/admin/views/AdminHub.vue'),
        },
        {
          path: 'admin/import',
          name: 'admin-import',
          component: () => import('@/features/admin/views/ImportPage.vue'),
        },
        {
          path: 'admin/templates',
          name: 'admin-templates',
          component: () => import('@/features/admin/views/TemplateList.vue'),
        },
        {
          path: 'admin/org',
          name: 'admin-org',
          component: () => import('@/features/admin/views/OrgSettings.vue'),
        },
        {
          path: 'admin/users',
          name: 'admin-users',
          component: () => import('@/features/admin/views/UserList.vue'),
        },
        {
          path: 'admin/billing',
          name: 'admin-billing',
          component: () => import('@/features/admin/views/BillingSettings.vue'),
        },
        {
          path: 'admin/categories',
          name: 'admin-categories',
          component: () => import('@/features/admin/views/CategoryList.vue'),
        },
        {
          path: 'admin/audit',
          name: 'admin-audit',
          component: () => import('@/features/admin/views/AuditLog.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(authGuard)

export default router
