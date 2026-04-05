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
        {
          path: 'notifications/preferences',
          name: 'notification-prefs',
          component: () => import('@/features/dashboard/views/NotificationPrefs.vue'),
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
          path: 'projects/transfer',
          name: 'project-transfer',
          component: () => import('@/features/projects/views/ProjectTransfer.vue'),
        },
        {
          path: 'projects/:id',
          name: 'project-detail',
          component: () => import('@/features/projects/views/ProjectDetail.vue'),
        },
        // Consortiums
        {
          path: 'consortiums',
          name: 'consortiums',
          component: () => import('@/features/consortiums/views/ConsortiumList.vue'),
        },
        {
          path: 'consortiums/new',
          name: 'consortium-create',
          component: () => import('@/features/consortiums/views/ConsortiumForm.vue'),
        },
        {
          path: 'consortiums/:id',
          name: 'consortium-detail',
          component: () => import('@/features/consortiums/views/ConsortiumDetail.vue'),
        },
        {
          path: 'consortiums/:id/edit',
          name: 'consortium-edit',
          component: () => import('@/features/consortiums/views/ConsortiumForm.vue'),
        },
        // Leaves
        {
          path: 'leaves',
          name: 'leaves',
          component: () => import('@/features/leaves/views/LeaveList.vue'),
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
        {
          path: 'period-locks',
          name: 'period-locks',
          component: () => import('@/features/timesheet/views/PeriodLocks.vue'),
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
        {
          path: 'credit-notes',
          name: 'credit-notes',
          component: () => import('@/features/billing/views/CreditNoteList.vue'),
        },
        {
          path: 'holdbacks',
          name: 'holdbacks',
          component: () => import('@/features/billing/views/HoldbackList.vue'),
        },
        {
          path: 'write-offs',
          name: 'write-offs',
          component: () => import('@/features/billing/views/WriteOffList.vue'),
        },
        // Expenses
        {
          path: 'expenses',
          name: 'expenses',
          component: () => import('@/features/expenses/views/ExpenseList.vue'),
        },
        {
          path: 'expenses/:id',
          name: 'expense-detail',
          component: () => import('@/features/expenses/views/ExpenseDetail.vue'),
        },
        // Suppliers
        {
          path: 'suppliers',
          name: 'suppliers',
          component: () => import('@/features/suppliers/views/SupplierList.vue'),
        },
        {
          path: 'suppliers/:id',
          name: 'supplier-detail',
          component: () => import('@/features/suppliers/views/SupplierDetail.vue'),
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
