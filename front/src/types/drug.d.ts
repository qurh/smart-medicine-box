// 药品信息类型
export interface Drug {
  name: string;
  indications?: string;
  usage?: string;
  contraindications?: string;
  precautions?: string;
  category?: string;
  expiration_date?: string;
  dosage_form?: string;
  specification?: string;
  [key: string]: any;
}

// 药品列表类型
export type DrugList = Drug[];

// 通用API响应类型
export interface ApiResponse<T = any> {
  code: number;
  msg: string;
  data: T;
}

// 查询药品信息请求
export interface ScanDrugRequest {
  drug_name: string;
}

// 保存药品信息请求（可直接用 Drug 类型）
// export type SaveDrugInfoRequest = Drug;
