import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './index.css'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import DrugList from './pages/DrugList.vue'
import SymptomSearch from './pages/SymptomSearch.vue'
import SymptomResults from './pages/SymptomResults.vue'
import DrugScan from './pages/DrugScan.vue'
import { createPinia } from 'pinia'

const routes = [
  { path: '/', component: Home },
  { path: '/drug-list', component: DrugList },
  { path: '/symptom-search', name: 'SymptomSearch', component: SymptomSearch },
  { path: '/symptom-results', name: 'SymptomResults', component: SymptomResults },
  { path: '/drug-scan', name: 'DrugScan', component: DrugScan }
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
