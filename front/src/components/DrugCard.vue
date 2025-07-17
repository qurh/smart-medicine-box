<script setup lang="ts">
import type { Drug } from '../types/drug'
import { getDrugFieldLabel, formatDate } from '../utils/format'
import { computed } from 'vue'

const props = defineProps<{ drug: Drug }>()
const fields = computed(() => Object.keys(props.drug).filter(k => k !== 'name'))
</script>

<template>
  <div class="drug-card">
    <h2 class="drug-title">{{ drug.name || '-' }}</h2>
    <div v-for="key in fields" :key="key" class="drug-field">
      <span class="drug-label">{{ getDrugFieldLabel(key) }}：</span>
      <span class="drug-value">
        <template v-if="key === 'expiration_date'">
          {{ formatDate(drug[key]) }}
        </template>
        <template v-else>
          {{ drug[key] || '-' }}
        </template>
      </span>
    </div>
    <slot />
  </div>
</template>

<style scoped>
.drug-card {
  background: linear-gradient(135deg, #e0e7ff 0%, #f7fafc 100%);
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(60, 120, 240, 0.10);
  padding: 28px 24px 20px 24px;
  display: flex;
  flex-direction: column;
  min-height: 220px;
  transition: box-shadow 0.2s, transform 0.2s;
  margin-bottom: 24px;
  border: 1.5px solid #e5e7eb;
}
.drug-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: #2563eb;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
.drug-field {
  display: flex;
  margin-bottom: 8px;
  font-size: 1rem;
}
.drug-label {
  font-weight: 600;
  color: #64748b;
  min-width: 90px;
  margin-right: 8px;
}
.drug-value {
  color: #22223b;
  word-break: break-all;
}
</style>
