import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './index.css'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import DrugList from './pages/DrugList.vue'
import { createPinia } from 'pinia'

const routes = [
  { path: '/', component: Home },
  { path: '/drug-list', component: DrugList }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(createPinia())
app.mount('#app')
