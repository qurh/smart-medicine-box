from pydantic import BaseModel
from typing import Optional

class Drug(BaseModel):
    name: str  # 药品名称
    indications: Optional[str] = None  # 主治功效
    usage: Optional[str] = None  # 用法用量
    contraindications: Optional[str] = None  # 禁忌症
    precautions: Optional[str] = None  # 注意事项
    category: Optional[str] = None  # 药品类别
    expiration_date: Optional[str] = None  # 失效日期
    dosage_form: Optional[str] = None  # 剂型
    specification: Optional[str] = None  # 规格