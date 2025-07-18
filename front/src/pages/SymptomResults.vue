<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchDrugsBySymptoms } from '../api/drug'
import DrugCard from '../components/DrugCard.vue'
import Loading from '../components/Loading.vue'
import ErrorAlert from '../components/ErrorAlert.vue'
import type { Drug } from '../types/drug'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const error = ref('')
const searchResults = ref<Drug[]>([])

const symptoms = computed(() => route.query.symptoms as string || '')

onMounted(async () => {
  // 检查是否有传递的查询结果
  const stateResults = history.state?.searchResults
  if (stateResults && stateResults.length > 0) {
    searchResults.value = stateResults
  } else if (symptoms.value) {
    // 如果没有传递结果但有症状参数，重新查询
    await performSearch()
  }
})

async function performSearch() {
  if (!symptoms.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const results = await searchDrugsBySymptoms(symptoms.value)
    searchResults.value = results
  } catch (err) {
    error.value = err instanceof Error ? err.message : '查询失败'
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.push({ name: 'SymptomSearch' })
}

// 分页逻辑
const pageSize = 8
const currentPage = ref(1)
const pagedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return searchResults.value.slice(start, start + pageSize)
})

function handlePageChange(page: number) {
  currentPage.value = page
}
</script>

<template>
  <div class="container mx-auto p-8 bg-gray-50 min-h-screen">
    <div class="mb-6">
      <el-button @click="goBack" type="text" class="mb-4">
        <el-icon><ArrowLeft /></el-icon>
        返回症状查询
      </el-button>
      
      <h1 class="text-3xl font-bold mb-2 text-center text-gray-700">查询结果</h1>
      <p v-if="symptoms" class="text-center text-gray-500 mb-8">
        症状：{{ symptoms }}
      </p>
    </div>

    <ErrorAlert v-if="error" :message="error" />
    <Loading v-else-if="loading" />
    <div v-else-if="!searchResults.length" class="text-center text-gray-500 mt-12">
      <p class="text-lg mb-4">未找到相关药品</p>
      <p class="text-sm">请尝试使用其他症状描述，或检查药箱中是否有相关药品</p>
      <el-button @click="goBack" type="primary" class="mt-4">
        重新查询
      </el-button>
    </div>
    <div v-else>
      <div class="mb-4 text-center text-gray-600">
        找到 {{ searchResults.length }} 个相关药品
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <DrugCard 
          v-for="(drug, idx) in pagedList" 
          :key="drug.name + idx" 
          :drug="drug" 
        />
      </div>
      
      <div class="flex justify-center mt-10" v-if="searchResults.length > pageSize">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="searchResults.length"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style> 