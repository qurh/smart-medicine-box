import type { Drug, ApiResponse, ScanDrugRequest } from '../types/drug'

// 通用安全fetch
async function safeFetch<T>(input: RequestInfo, init?: RequestInit): Promise<ApiResponse<T>> {
  try {
    const resp = await fetch(input, init)
    if (!resp.ok) {
      throw new Error('服务暂不可用，请稍后重试或联系管理员')
    }
    try {
      return await resp.json()
    } catch {
      throw new Error('服务响应异常，请稍后重试')
    }
  } catch (e: any) {
    throw new Error(e.message || '网络异常，请检查后端服务是否启动')
  }
}

// 查询药箱列表
export async function getDrugList(): Promise<Drug[]> {
  const res = await safeFetch<Drug[]>('/api/drug/list')
  if (res.code !== 0) throw new Error(res.msg || '获取药品列表失败')
  return res.data || []
}

// 查询药品信息
export async function scanDrug(payload: ScanDrugRequest): Promise<Drug> {
  const res = await safeFetch<Drug>('/api/drug/scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (res.code !== 0) throw new Error(res.msg || '查询药品信息失败')
  return res.data
}

// 保存药品信息到药箱
export async function saveDrugInfo(drug: Drug): Promise<void> {
  const res = await safeFetch('/api/drug/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(drug)
  })
  if (res.code !== 0) throw new Error(res.msg || '保存药品信息失败')
}

// 根据症状查询药品
export async function searchDrugsBySymptoms(symptoms: string, topK: number = 3): Promise<Drug[]> {
  const res = await safeFetch<Drug[]>('/api/drug/search-by-symptoms', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms, top_k: topK })
  })
  if (res.code !== 0) throw new Error(res.msg || '症状查询失败')
  return res.data || []
}
