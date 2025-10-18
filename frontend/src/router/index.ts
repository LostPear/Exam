import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes: RouteRecordRaw[] = [
  { path: '/', redirect: '/auth/login' },
  {
    path: '/auth',
    component: () => import('../views/auth/AuthLayout.vue'),
    children: [
      { path: 'login', name: 'login', component: () => import('../views/auth/Login.vue') },
      { path: 'register', name: 'register', component: () => import('../views/auth/Register.vue') },
    ],
  },
  {
    path: '/app',
    component: () => import('../views/app/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/app/practice' },
      { path: 'practice', name: 'practice', component: () => import('../views/app/Practice.vue') },
      { path: 'exam', name: 'exam', component: () => import('../views/app/Exam.vue') },
      { path: 'profile', name: 'profile', component: () => import('../views/app/Profile.vue') },
      { path: 'practice/session', name: 'practice-session', component: () => import('../views/app/PracticeSession.vue') },
      { path: 'exam/session', name: 'exam-session', component: () => import('../views/app/ExamSession.vue') },
    ],
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', redirect: '/admin/questions' },
      { path: 'questions', name: 'admin-questions', component: () => import('../views/admin/Questions.vue') },
      { path: 'users', name: 'admin-users', component: () => import('../views/admin/Users.vue') },
      { path: 'import', name: 'admin-import', component: () => import('../views/admin/Import.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requiresAdmin && !auth.currentUser?.is_admin) {
    return { name: 'practice' }
  }
})

export default router
