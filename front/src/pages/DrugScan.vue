<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMedicineBoxStore } from '../stores/medicineBox'
import { scanDrug } from '../api/drug'
import DrugForm from '../components/DrugForm.vue'
import DrugCard from '../components/DrugCard.vue'
import Loading from '../components/Loading.vue'
import ErrorAlert from '../components/ErrorAlert.vue'
import type { Drug, ScanDrugRequest } from '../types/drug'

const store = useMedicineBoxStore()
const router = useRouter()

const isQueryLoading = ref(false)
const isAddLoading = ref(false)
const error = ref<string | null>(null)
const drugInfo = ref<Drug | null>(null)

async function handleScan(payload: ScanDrugRequest) {
  isQueryLoading.value = true
  error.value = null
  drugInfo.value = null
  try {
    const res = await scanDrug(payload)
    drugInfo.value = res
  } catch (e: any) {
    error.value = e.message || '查询失败'
  } finally {
    isQueryLoading.value = false
  }
}

async function handleAddToBox() {
  if (!drugInfo.value) return
  isAddLoading.value = true
  error.value = null
  try {
    await store.addDrug(drugInfo.value)
    router.push('/drug-list')
  } catch (e: any) {
    error.value = e.message || '保存失败'
  } finally {
    isAddLoading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto p-8 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-8 text-center text-gray-700">药品扫描</h1>
    <div class="max-w-lg mx-auto bg-white rounded-xl shadow-lg p-8">
      <DrugForm @submit="handleScan" :loading="isQueryLoading" />
    </div>
    <ErrorAlert v-if="error" :message="error" />
    <Loading v-else-if="isQueryLoading" />
    <div v-if="drugInfo" class="max-w-lg mx-auto mt-6">
      <DrugCard :drug="drugInfo" />
      <div class="flex justify-center mt-8">
        <el-button type="primary" size="large" @click="handleAddToBox" :disabled="isAddLoading" style="font-size: 22px; padding: 16px 48px;">
          放入家庭药箱
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style> 