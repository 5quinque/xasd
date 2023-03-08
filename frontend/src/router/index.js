import { createRouter, createWebHistory } from 'vue-router'
import XasdView from '../views/XasdView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: XasdView
        },
        {
            path: '/search',
            name: 'search',
            // route level code-splitting
            // this generates a separate chunk (About.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('../views/XasdView.vue')
        },
        {
            path: '/queue',
            name: 'queue',
            // route level code-splitting
            // this generates a separate chunk (About.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('../views/XasdView.vue')
        }
    ]
})

export default router
