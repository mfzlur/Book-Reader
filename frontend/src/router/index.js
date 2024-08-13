import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserLogin from '@/authorization/UserLogin.vue'
import UserRegister from '@/authorization/UserRegister.vue'
import UserDashboard from '../views/UserDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: UserLogin
    },
    {
      path: '/register',
      name: 'register',
      component: UserRegister
    },
    
    {
      path: '/user/dashboard',
      name: 'userDashboard',
      component: UserDashboard
    },
    {
      path: '/librarian/dashboard',
      name: 'librarianDashboard',
      component: () => import('../views/LibrarianDashboard.vue')
    },
    {
      path: '/add/book',
      name: 'addBook',
      component: () => import('../components/AddBook.vue')
    },
    {
      path: '/add/section',
      name: 'addSection',
      component: () => import('../components/AddSection.vue')
    },
    {
      path: '/edit/book/:id',
      name: 'editBook',
      component: () => import('../components/EditBook.vue')
    },
    {
      path: '/edit/section/:id',
      name: 'editSection',
      component: () => import('../components/EditSection.vue')
    },
    { 
      path: '/all/books',
      name: 'allBooks',
      component: () => import('../views/AllBooks.vue')
    },
    { 
      path: '/pending/requests',
      name: 'bookRequests',
      component: () => import('../views/BookRequests.vue')
    },
    { 
      path: '/my/books',
      name: 'myBooks',
      component: () => import('../views/MyBooks.vue')
    },
    {
      path: '/search/',
      name: 'search',
      component: () => import('../views/SearchPage.vue')
    },
    {
      path: '/book/:id',
      name: 'BookDetails',
      component: () => import('../views/BookDetails.vue')
    },
    {
      path: '/section/:id',
      name: 'SectionDetails',
      component: () => import('../views/SectionDetails.vue')
    },
    {
      path: '/bar/chart',
      name: 'BarChartComponent',
      component: () => import('../views/BarChart.vue')
    },
    {
      path: '/pie/chart',
      name: 'PieChartComponent',
      component: () => import('../views/PieChart.vue')
    },
    {
      path: '/librarian/stats',
      name: 'librarianStats',
      component: () => import('../views/LibrarianStats.vue')
    },
    {
      path: '/pdf/upload',
      name: 'pdfUpload',
      component: () => import('../components/PdfUpload.vue')
    },
    { 
      path: '/celery/mail',
      name: 'celeryMail',
      component: () => import('../components/CeleryMail.vue')
    },
    {
      path: '/export/csv',
      name: 'exportCSV',
      component: () => import('../components/ExportCsv.vue')
    },
    {
      path: '/export/pdf',
      name: 'exportPDF',
      component: () => import('../components/PdfViewer.vue')
    }
 
  ]
})

export default router
