from pydantic import BaseModel
from app.schemas.base_request import BaseRequest
from typing import Optional

class ScanRequest(BaseRequest):
    drug_name: str

class SaveDrugInfoRequest(BaseRequest):
    name: str
    indications: Optional[str] = None
    usage: Optional[str] = None
    contraindications: Optional[str] = None
    precautions: Optional[str] = None
    category: Optional[str] = None
    expiration_date: Optional[str] = None
    dosage_form: Optional[str] = None
    specification: Optional[str] = None

class DrugListRequest(BaseRequest):
    # 预留分页参数
    page: Optional[int] = 1
    size: Optional[int] = 20

class SymptomSearchRequest(BaseRequest):
    symptoms: str
    top_k: Optional[int] = 3