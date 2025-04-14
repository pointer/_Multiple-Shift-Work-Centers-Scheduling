import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Employees from '../views/Employees.vue'
import WorkCenters from '../views/WorkCenters.vue'
import Schedule from '../views/Schedule.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/employees',
    name: 'Employees',
    component: Employees
  },
  {
    path: '/work-centers',
    name: 'WorkCenters',
    component: WorkCenters
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router