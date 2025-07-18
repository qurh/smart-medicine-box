import os
from app.prompts.drug_info_extract import DRUG_INFO_EXTRACT_PROMPT
from app.models.drug import Drug
from langchain_community.llms import Tongyi
from app.core.config import QWEN3_API_KEY
from app.utils.field_map import CN2EN
from app.services.mock_service import get_mock_drug_info
import json

# 初始化 LLM
os.environ["DASHSCOPE_API_KEY"] = QWEN3_API_KEY
llm = Tongyi(model_name="qwen-plus", temperature=0.7)

def enrich_drug_info_llm(drug_name: str) -> Drug:
    prompt = DRUG_INFO_EXTRACT_PROMPT.format(drug_name=drug_name)
    # 1. 调用大模型
    result = llm(prompt)
    # 2. 解析模型输出
    try:
        data_cn = json.loads(result)
    except Exception as e:
        raise ValueError(f"模型输出解析失败: {e}, 原始输出: {result}")
    # 3. 中文键转英文键
    data_en = {CN2EN[k]: v for k, v in data_cn.items() if k in CN2EN}
    # 4. 返回 Drug 实例
    return Drug(**data_en)

def enrich_drug_info_mock(drug_name: str) -> Drug:
    return get_mock_drug_info(drug_name)