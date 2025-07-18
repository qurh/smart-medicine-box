from fastapi import APIRouter, HTTPException
from app.models.drug import Drug
from app.services.drug_info_process import enrich_drug_info_llm, enrich_drug_info_mock
from app.services.medicine_box_service import save_drug_to_box, get_medicine_box_list
from app.services.vector_search_service import vector_search_service
from app.schemas.requests import ScanRequest, SaveDrugInfoRequest, SymptomSearchRequest
from app.schemas.base_response import BaseResponse
from app.core.config import USE_MOCK_DATA
import random

router = APIRouter(prefix="/drug", tags=["药品管理"])

@router.post("/scan", response_model=BaseResponse)
def scan_drug(req: ScanRequest):
    if not req.drug_name:
        raise HTTPException(status_code=400, detail="drug_name 不能为空")
    if USE_MOCK_DATA:
        drug_info = enrich_drug_info_mock(req.drug_name)
    else:
        drug_info = enrich_drug_info_llm(req.drug_name)
    return BaseResponse(data=drug_info)

@router.post("/save", response_model=BaseResponse)
def add_drug_to_box(req: SaveDrugInfoRequest):
    drug = Drug(**req.model_dump())
    if USE_MOCK_DATA:
        save_drug_to_box(drug)
    else:
        # 保存药品信息到向量数据库
        vector_search_service.add_drug_embedding(drug)
    return BaseResponse(msg="保存成功")

@router.get("/list", response_model=BaseResponse)
def get_drug_list():
    if USE_MOCK_DATA:
        data = get_medicine_box_list()
    else:
        data = vector_search_service.get_all_drugs_from_vector_db()
    return BaseResponse(data=data)

@router.post("/search-by-symptoms", response_model=BaseResponse)
def search_drugs_by_symptoms(req: SymptomSearchRequest):
    if not req.symptoms:
        raise HTTPException(status_code=400, detail="symptoms 不能为空")
    
    top_k = req.top_k or 3
    if USE_MOCK_DATA:
        all_drugs = get_medicine_box_list()
        results = random.sample(all_drugs, min(top_k, len(all_drugs))) if all_drugs else []
    else:
        results = vector_search_service.search_by_symptoms(req.symptoms, top_k)
    return BaseResponse(data=results)