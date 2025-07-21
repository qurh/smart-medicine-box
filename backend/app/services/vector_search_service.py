import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from app.models.drug import Drug
from app.services.medicine_box_service import get_medicine_box_list
from loguru import logger
from app.core.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, get_settings
import chromadb
from chromadb.utils import embedding_functions
import json
import os
import requests

class EmbeddingProvider:
    CLOUD = "cloud_bge_m3"
    LOCAL = "local_model"

class VectorSearchService:
    def __init__(self):
        settings = get_settings() if callable(get_settings) else get_settings
        self.embedding_provider = getattr(settings, "EMBEDDING_PROVIDER", EmbeddingProvider.CLOUD)
        chroma_dir = str(CHROMA_PERSIST_DIR)
        print(f"[ChromaDB] 持久化目录: {chroma_dir}")
        if not os.path.exists(chroma_dir):
            print(f"[ChromaDB] 持久化目录不存在，将自动创建: {chroma_dir}")
            os.makedirs(chroma_dir, exist_ok=True)
        else:
            files = os.listdir(chroma_dir)
            # 更健壮的数据文件检测
            key_files = ['chroma.sqlite3', 'manifest.json', 'chroma-collections.parquet']
            data_files = [f for f in files if os.path.isfile(os.path.join(chroma_dir, f)) and os.path.getsize(os.path.join(chroma_dir, f)) > 0]
            if not any(f in files for f in key_files) and not data_files:
                print(f"[ChromaDB] 警告：持久化目录下无典型ChromaDB数据文件或有效数据文件，可能未持久化！")
            else:
                print(f"[ChromaDB] 检测到数据文件: {data_files if data_files else files}")
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME
        )
        logger.info(f"Chroma collection: {CHROMA_COLLECTION_NAME}, embedding provider: {self.embedding_provider}")
        # 本地模型初始化（仅本地模式用）
        if self.embedding_provider == EmbeddingProvider.LOCAL:
            self.model_path = getattr(settings, "EMBEDDING_MODEL_PATH", r"D:\\projects\\models\\paraphrase-multilingual-MiniLM-L12-v2")
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_path)

    def add_drug_embedding(self, drug: Drug):
        """将药品主治功效字段向量化并存入chroma，元数据为药品名称和完整json"""
        if not drug.indications:
            logger.warning(f"药品 {drug.name} 缺少主治功效字段，跳过向量嵌入")
            return
        # 预处理主治功效字段：只保留前3个核心症状/疾病词
        indications = drug.indications
        for sep in ['，', '、', ';', '；', ',', '/']:
            indications = indications.replace(sep, '|')
        keywords = [w.strip() for w in indications.split('|') if w.strip()]
        core_indications = '，'.join(keywords[:3]) if keywords else drug.indications
        # 以药品名称为唯一id
        doc_id = drug.name
        # 元数据包含药品名称和完整json
        metadata = {
            "name": drug.name,
            "drug_json": drug.model_dump_json()
        }
        # 先删除同名旧向量
        self.collection.delete(ids=[doc_id])
        # 生成 embedding（根据配置自动切换）
        embedding = self.get_embedding([core_indications])[0]
        # 添加新向量
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[core_indications],
            metadatas=[metadata]
        )
        logger.info(f"已向量化并存入Chroma: {drug.name} | 主治功效关键词: {core_indications}")

    def search_by_symptoms(self, symptoms: str, top_k: int = 5, min_score: float = 0.5) -> List[Dict[str, Any]]:
        """
        用症状文本向量化后在chroma中检索，返回药品元数据列表
        """
        if not symptoms:
            return []
        try:
            results = self.collection.query(
                query_texts=[symptoms],
                n_results=top_k,
                include=["metadatas", "distances"]
            )
            metadatas = results.get('metadatas') or []
            distances = results.get('distances') or []
            if not metadatas or not distances or not isinstance(metadatas, list) or not isinstance(distances, list):
                return []
            metadatas = metadatas[0] if len(metadatas) > 0 else []
            distances = distances[0] if len(distances) > 0 else []
            filtered = [
                json.loads(meta['drug_json'])
                for meta, dist in zip(metadatas, distances)
                if 'drug_json' in meta and isinstance(meta['drug_json'], str) and dist >= min_score
            ]
            return filtered
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
            return list(reversed(all_drugs))
        except Exception as e:
            logger.error(f"Chroma 全量获取失败: {e}")
            return []

    def get_embedding(self, texts: list[str]) -> list:
        if self.embedding_provider == EmbeddingProvider.LOCAL:
            return self.get_local_embedding(texts)
        else:
            return self.get_bge_m3_embedding(texts)

    def get_local_embedding(self, texts: list[str]) -> list:
        """本地模型 embedding，支持批量"""
        return [self.model.encode(t).tolist() for t in texts]

    def get_bge_m3_embedding(self, texts: list[str]) -> list:
        """云端 bge-m3 embedding 服务，支持批量"""
        url = "http://61.169.22.138:10004/v1/embeddings"
        payload = {
            "model": "bge-m3",
            "input": texts
        }
        try:
            resp = requests.post(url, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if (
                isinstance(data, dict)
                and "data" in data
                and isinstance(data["data"], list)
                and len(data["data"]) == len(texts)
            ):
                return [item["embedding"] for item in data["data"]]
            else:
                raise ValueError(f"云端 embedding 服务返回格式异常: {data}")
        except Exception as e:
            logger.error(f"bge-m3 embedding 云端服务调用失败: {e}")
            raise

# 全局实例
vector_search_service = VectorSearchService()

def detect_chromadb_persistence():
    chroma_dir = str(CHROMA_PERSIST_DIR)
    print(f"[ChromaDB] 检查持久化目录: {chroma_dir}")
    if not os.path.exists(chroma_dir):
        print(f"[ChromaDB] 持久化目录不存在，自动创建: {chroma_dir}")
        os.makedirs(chroma_dir, exist_ok=True)
        return False
    files = os.listdir(chroma_dir)
    data_files = [f for f in files if f.endswith(('.parquet', '.bin', '.json'))]
    if not data_files:
        print(f"[ChromaDB] 持久化目录下无数据文件，可能未持久化！")
        return False
    print(f"[ChromaDB] 检测到数据文件: {data_files}")
    return True

if __name__ == "__main__":
    print("[ChromaDB] 自动检测与修复持久化目录...")
    detect_chromadb_persistence() 