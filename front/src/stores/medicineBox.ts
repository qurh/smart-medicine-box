import { defineStore } from 'pinia'
import type { Drug } from '../types/drug'
import { getDrugList, saveDrugInfo } from '../api/drug'

interface State {
  drugList: Drug[]
  loading: boolean
  error: string | null
}

export const useMedicineBoxStore = defineStore('medicineBox', {
  state: (): State => ({
    drugList: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchDrugList() {
      this.loading = true
      this.error = null
      try {
        const list = await getDrugList()
        this.drugList = list
      } catch (e: any) {
        this.error = e.message || '获取药品列表失败'
        this.drugList = []
      } finally {
        this.loading = false
      }
    },
    async addDrug(drug: Drug) {
      this.loading = true
      this.error = null
      try {
        await saveDrugInfo(drug)
        await this.fetchDrugList() // 保存后刷新列表
      } catch (e: any) {
        this.error = e.message || '保存药品失败'
      } finally {
        this.loading = false
      }
    }
  }
})
