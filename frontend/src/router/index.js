import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Login from '../views/Login.vue'
import StoreSelection from '../views/StoreSelection.vue'
import WithdrawalForm from '../views/WithdrawalForm.vue'
import Reports from '../views/Reports.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { guestOnly: true }
    },
    {
        path: '/',
        name: 'StoreSelection',
        component: StoreSelection,
        meta: { requiresAuth: true }
    },
    {
        path: '/withdraw/:storeId',
        name: 'WithdrawalForm',
        component: WithdrawalForm,
        meta: { requiresAuth: true }
    },
    {
        path: '/reports',
        name: 'Reports',
        component: Reports,
        meta: { requiresAuth: true, roles: ['MASTER', 'RELATORIO'] }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    if (localStorage.getItem('access_token') && !authStore.user) {
        await authStore.fetchUser()
    }

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.meta.guestOnly && authStore.isAuthenticated) {
        next('/')
    } else if (to.meta.roles && authStore.user && !to.meta.roles.includes(authStore.user.role)) {
        next('/') // Redirect to home if no permission
    } else {
        next()
    }
})

export default router
