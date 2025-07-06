// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },

  // 可以在此添加其他页面，如分析页
  // {
  //   path: '/analysis',
  //   name: 'Analysis',
  //   component: () => import('@/views/AnalysisView.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
