// 日期格式化（yyyy-mm-dd）
export function formatDate(dateStr?: string): string {
  if (!dateStr) return '-';
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr;
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

// 药品字段中英文映射
export const drugFieldMap: Record<string, string> = {
  name: '药品名称',
  indications: '主治功效',
  usage: '用法用量',
  contraindications: '禁忌症',
  precautions: '注意事项',
  category: '药品类别',
  expiration_date: '失效日期',
  dosage_form: '剂型',
  specification: '规格',
}

// 获取字段中文名
export function getDrugFieldLabel(key: string): string {
  return drugFieldMap[key] || key
}
