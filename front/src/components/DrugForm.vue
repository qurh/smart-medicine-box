<script setup lang="ts">
import { ref } from 'vue'
import type { ScanDrugRequest } from '../types/drug'
import { ElForm, ElFormItem, ElInput, ElButton } from 'element-plus'

const emit = defineEmits<{ (e: 'submit', payload: ScanDrugRequest): void }>()
const drugName = ref('')
const isLoading = defineModel<boolean>('loading', { default: false })

function onSubmit() {
  if (!drugName.value) return
  emit('submit', { drug_name: drugName.value })
}
</script>

<template>
  <el-form @submit.prevent="onSubmit" label-position="left">
    <el-form-item label="药品名称" class="form-label-item">
      <el-input v-model="drugName" placeholder="请输入药品名称" size="large" clearable />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit" :loading="isLoading" class="w-full" size="large">
        {{ isLoading ? '查询中...' : '确认查询' }}
      </el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped>
.form-label-item :deep(.el-form-item__label) {
  font-size: 1.15rem;
  font-weight: 600;
  color: #22223b;
  min-width: 90px;
  text-align: left;
  display: flex;
  align-items: center;
  padding-right: 12px;
}
</style>
