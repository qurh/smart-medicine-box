import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from app.models.drug import Drug
from app.services.medicine_box_service import get_medicine_box_list
from loguru import logger
from app.core.config import VECTOR_MODEL_NAME, CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json

class VectorSearchService:
    def __init__(self):
        # 支持模型可配置
        self.model_name = VECTOR_MODEL_NAME
        self.model = SentenceTransformer(self.model_name)
        self.chroma_client = chromadb.Client(Settings(persist_directory=CHROMA_PERSIST_DIR))
        self.collection = self.chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME
        )
        logger.info(f"向量模型: {self.model_name}, Chroma collection: {CHROMA_COLLECTION_NAME}")

    def add_drug_embedding(self, drug: Drug):
        """将药品主治功效字段向量化并存入chroma，元数据为药品名称和完整json"""
        if not drug.indications:
            logger.warning(f"药品 {drug.name} 缺少主治功效字段，跳过向量嵌入")
            return
        # 以药品名称为唯一id
        doc_id = drug.name
        # 元数据包含药品名称和完整json
        metadata = {
            "name": drug.name,
            "drug_json": drug.model_dump_json()
        }
        # 先删除同名旧向量
        self.collection.delete(ids=[doc_id])
        # 添加新向量
        self.collection.add(
            ids=[doc_id],
            documents=[drug.indications],
            metadatas=[metadata]
        )
        logger.info(f"已向量化并存入Chroma: {drug.name}")

    def search_by_symptoms(self, symptoms: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        用症状文本向量化后在chroma中检索，返回药品元数据列表
        """
        if not symptoms:
            return []
        try:
            results = self.collection.query(
                query_texts=[symptoms],
                n_results=top_k
            )
            # 解析元数据
            metadatas = results.get('metadatas', [])
            if not metadatas:
                return []
            metadatas = metadatas[0]
            # 返回药品信息json
            return [json.loads(meta['drug_json']) for meta in metadatas if 'drug_json' in meta and isinstance(meta['drug_json'], str)]
        except Exception as e:
            logger.error(f"Chroma 检索失败: {e}")
            return []

    def refresh_embeddings(self):
        """重建所有药品的向量索引（全量重建）"""
        logger.info("重建所有药品的向量索引")
        self.collection.delete(where={})
        drug_list = get_medicine_box_list()
        for drug in drug_list:
            try:
                self.add_drug_embedding(Drug(**drug))
            except Exception as e:
                logger.warning(f"药品向量化失败: {e}")

    def get_all_drugs_from_vector_db(self) -> list[dict]:
        """获取向量数据库中所有药品元数据（反序列化drug_json）"""
        try:
            results = self.collection.get()
            metadatas = results.get('metadatas', [])
            if not metadatas:
                return []
            all_drugs = []
            for meta in metadatas:
                if isinstance(meta, dict) and 'drug_json' in meta and isinstance(meta['drug_json'], str):
                    try:
                        all_drugs.append(json.loads(meta['drug_json']))
                    except Exception:
                        pass
            return all_drugs
        except Exception as e:
            logger.error(f"Chroma 全量获取失败: {e}")
            return []

# 全局实例
vector_search_service = VectorSearchService() 