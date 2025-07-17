<script setup lang="ts">
defineProps<{ text?: string }>()
</script>
<template>
  <div class="flex flex-col items-center justify-center py-8 text-gray-500">
    <span class="loader mb-2"></span>
    <span>{{ text || '加载中...' }}</span>
  </div>
</template>
<style scoped>
.loader {
  border: 4px solid #e0e7ff;
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
