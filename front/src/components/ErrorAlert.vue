<script setup lang="ts">
defineProps<{ message: string }>()
</script>
<template>
  <div v-if="message" class="max-w-lg mx-auto mt-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative" role="alert">
    <strong class="font-bold">出错了: </strong>
    <span class="block sm:inline">{{ message }}</span>
  </div>
</template>
