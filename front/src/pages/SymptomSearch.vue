<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { searchDrugsBySymptoms } from '../api/drug'
import Loading from '../components/Loading.vue'
import ErrorAlert from '../components/ErrorAlert.vue'

const router = useRouter()
const symptoms = ref('')
const loading = ref(false)
const error = ref('')

// 常见症状建议
const commonSymptoms = [
  '头痛', '发烧', '咳嗽', '感冒', '胃痛', '腹泻', '失眠', '过敏',
  '关节痛', '牙痛', '咽喉痛', '鼻塞', '流鼻涕', '恶心', '呕吐'
]

async function handleSearch() {
  if (!symptoms.value.trim()) {
    error.value = '请输入症状描述'
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    const results = await searchDrugsBySymptoms(symptoms.value.trim())
    // 跳转到结果页面，传递查询结果
    router.push({
      name: 'SymptomResults',
      query: { symptoms: symptoms.value.trim() },
      state: { searchResults: results }
    })
  } catch (err) {
    error.value = err instanceof Error ? err.message : '查询失败'
  } finally {
    loading.value = false
  }
}

function selectSymptom(symptom: string) {
  symptoms.value = symptom
}
</script>

<template>
  <div class="container mx-auto p-8 bg-gray-50 min-h-screen">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-center text-gray-700">症状查询</h1>
      
      <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            请描述您的症状
          </label>
          <el-input
            v-model="symptoms"
            type="textarea"
            :rows="4"
            placeholder="例如：我最近经常头痛，特别是下午的时候..."
            class="w-full"
            @keyup.enter="handleSearch"
          />
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold mb-3 text-gray-700">常见症状</h3>
          <div class="flex flex-wrap gap-2">
            <el-tag
              v-for="symptom in commonSymptoms"
              :key="symptom"
              @click="selectSymptom(symptom)"
              class="cursor-pointer hover:bg-blue-100"
              type="info"
            >
              {{ symptom }}
            </el-tag>
          </div>
        </div>

        <ErrorAlert v-if="error" :message="error" />
        
        <div class="flex justify-center">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleSearch"
            class="px-8"
          >
            {{ loading ? '查询中...' : '查询相关药品' }}
          </el-button>
        </div>
      </div>

      <div class="mt-8 text-center text-gray-500 text-sm">
        <p>💡 检索建议：请只输入最核心的症状或疾病关键词（如“发热、咳嗽、头痛”），避免长句和无关描述，这样更容易获得准确的药品推荐。</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style> 