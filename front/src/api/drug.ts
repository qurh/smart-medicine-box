import type { Drug, ApiResponse, ScanDrugRequest } from '../types/drug'

// 查询药箱列表
export async function getDrugList(): Promise<Drug[]> {
  const resp = await fetch('/api/drug/list')
  const res: ApiResponse<Drug[]> = await resp.json()
  if (res.code !== 0) throw new Error(res.msg || '获取药品列表失败')
  return res.data || []
}

// 查询药品信息
export async function scanDrug(payload: ScanDrugRequest): Promise<Drug> {
  const resp = await fetch('/api/drug/scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  const res: ApiResponse<Drug> = await resp.json()
  if (res.code !== 0) throw new Error(res.msg || '查询药品信息失败')
  return res.data
}

// 保存药品信息到药箱
export async function saveDrugInfo(drug: Drug): Promise<void> {
  const resp = await fetch('/api/drug/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(drug)
  })
  const res: ApiResponse = await resp.json()
  if (res.code !== 0) throw new Error(res.msg || '保存药品信息失败')
}
