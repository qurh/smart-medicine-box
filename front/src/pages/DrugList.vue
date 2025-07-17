<script setup lang="ts">
import { onMounted, watch, computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMedicineBoxStore } from '../stores/medicineBox'
import DrugCard from '../components/DrugCard.vue'
import Loading from '../components/Loading.vue'
import ErrorAlert from '../components/ErrorAlert.vue'

const store = useMedicineBoxStore()
const route = useRoute()

onMounted(() => {
  store.fetchDrugList()
})

watch(
  () => route.fullPath,
  () => {
    store.fetchDrugList()
  }
)

const pageSize = 8
const currentPage = ref(1)
const pagedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return store.drugList.slice(start, start + pageSize)
})
function handlePageChange(page: number) {
  currentPage.value = page
}
</script>

<template>
  <div class="container mx-auto p-8 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-8 text-center text-gray-700">药品列表</h1>
    <ErrorAlert v-if="store.error" :message="store.error" />
    <Loading v-else-if="store.loading" />
    <div v-else-if="!store.drugList.length" class="text-center text-gray-500 mt-12">暂无药品，请先添加。</div>
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <DrugCard v-for="(drug, idx) in pagedList" :key="drug.name + idx" :drug="drug" />
      </div>
      <div class="flex justify-center mt-10" v-if="store.drugList.length > pageSize">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="store.drugList.length"
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