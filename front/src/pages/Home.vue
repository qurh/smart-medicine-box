<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToSymptomSearch() {
  router.push('/symptom-search')
}
function goToDrugList() {
  router.push('/drug-list')
}
function goToDrugScan() {
  router.push('/drug-scan')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex flex-col">
    <h1 class="text-4xl md:text-5xl font-extrabold mb-12 mt-10 text-center text-gray-800 tracking-wide drop-shadow-lg">家庭智能药箱</h1>
    <div class="flex-1 flex flex-col items-center justify-center">
      <div class="w-full max-w-lg px-4 flex flex-col gap-10">
        <!-- 症状查询卡片 -->
        <div
          class="bg-white rounded-3xl shadow-2xl p-10 flex flex-col items-center transition-all duration-200 hover:-translate-y-2 hover:shadow-3xl cursor-pointer"
          @click="goToSymptomSearch"
        >
          <div class="w-16 h-16 flex items-center justify-center mb-6">
            <svg width="56" height="56" viewBox="0 0 64 64" fill="none">
              <circle cx="32" cy="32" r="28" fill="url(#symptom-gradient)"/>
              <path d="M32 18a10 10 0 1 1 0 20a10 10 0 0 1 0-20z" fill="#fff"/>
              <path d="M32 38v8" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
              <circle cx="32" cy="50" r="2.5" fill="#2563eb"/>
              <defs>
                <linearGradient id="symptom-gradient" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#60a5fa"/>
                  <stop offset="1" stop-color="#a78bfa"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="text-xl font-bold text-gray-800 mb-1">症状查询</div>
          <div class="text-gray-500 text-center">根据症状查找相关药品</div>
        </div>
        <!-- 药箱管理卡片 -->
        <div
          class="bg-white rounded-3xl shadow-2xl p-10 flex flex-col items-center transition-all duration-200 hover:-translate-y-2 hover:shadow-3xl cursor-pointer"
          @click="goToDrugList"
        >
          <div class="w-16 h-16 flex items-center justify-center mb-6">
            <svg width="56" height="56" viewBox="0 0 64 64" fill="none">
              <rect x="8" y="16" width="48" height="32" rx="8" fill="url(#box-gradient)"/>
              <rect x="20" y="28" width="24" height="8" rx="2" fill="#fff"/>
              <rect x="28" y="36" width="8" height="8" rx="2" fill="#fff"/>
              <defs>
                <linearGradient id="box-gradient" x1="8" y1="16" x2="56" y2="48" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#fbbf24"/>
                  <stop offset="1" stop-color="#fb7185"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="text-xl font-bold text-gray-800 mb-1">药箱管理</div>
          <div class="text-gray-500 text-center">查看和管理家庭药箱</div>
        </div>
        <!-- 药品扫描卡片 -->
        <div
          class="bg-white rounded-3xl shadow-2xl p-10 flex flex-col items-center transition-all duration-200 hover:-translate-y-2 hover:shadow-3xl cursor-pointer"
          @click="goToDrugScan"
        >
          <div class="w-16 h-16 flex items-center justify-center mb-6">
            <svg width="56" height="56" viewBox="0 0 64 64" fill="none">
              <rect x="12" y="12" width="40" height="40" rx="8" fill="url(#scan-gradient)"/>
              <rect x="24" y="28" width="16" height="8" rx="2" fill="#fff"/>
              <rect x="30" y="36" width="4" height="8" rx="2" fill="#fff"/>
              <rect x="38" y="36" width="4" height="8" rx="2" fill="#fff"/>
              <defs>
                <linearGradient id="scan-gradient" x1="12" y1="12" x2="52" y2="52" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#fb7185"/>
                  <stop offset="1" stop-color="#a78bfa"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="text-xl font-bold text-gray-800 mb-1">药品扫描</div>
          <div class="text-gray-500 text-center">扫描药品条码或输入药品名称</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style> 