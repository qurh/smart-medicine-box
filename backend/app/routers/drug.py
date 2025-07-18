from fastapi import APIRouter, HTTPException
from app.models.drug import Drug
from app.services.drug_info_process import enrich_drug_info
from app.services.medicine_box_service import save_drug_to_box, get_medicine_box_list
from app.services.vector_search_service import vector_search_service
from app.schemas.requests import ScanRequest, SaveDrugInfoRequest, SymptomSearchRequest
from app.schemas.base_response import BaseResponse

router = APIRouter(prefix="/drug", tags=["药品管理"])

@router.post("/scan", response_model=BaseResponse)
def scan_drug(req: ScanRequest):
    if not req.drug_name:
        raise HTTPException(status_code=400, detail="drug_name 不能为空")
    drug_info = enrich_drug_info(req.drug_name)
    return BaseResponse(data=drug_info)

@router.post("/save", response_model=BaseResponse)
def add_drug_to_box(req: SaveDrugInfoRequest):
    drug = Drug(**req.model_dump())
    save_drug_to_box(drug)
    # 保存药品后增量向量嵌入
    vector_search_service.add_drug_embedding(drug)
    return BaseResponse(msg="保存成功")

@router.get("/list", response_model=BaseResponse)
def get_drug_list():
    data = get_medicine_box_list()
    return BaseResponse(data=data)

@router.post("/search-by-symptoms", response_model=BaseResponse)
def search_drugs_by_symptoms(req: SymptomSearchRequest):
    if not req.symptoms:
        raise HTTPException(status_code=400, detail="symptoms 不能为空")
    
    top_k = req.top_k or 5
    results = vector_search_service.search_by_symptoms(req.symptoms, top_k)
    return BaseResponse(data=results) 