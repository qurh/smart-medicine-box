from typing import List, Dict, Any
from app.models.drug import Drug
from app.services.medicine_box_service import get_medicine_box_list
from loguru import logger
from app.core.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, get_settings, DASHSCOPE_API_KEY
import chromadb
import json
import os
import requests
import dashscope
from http import HTTPStatus

class EmbeddingProvider:
    CLOUD = "cloud_bge_m3"
    TEXT_EMBEDDING_V4 = "text-embedding-v4"

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
        # text-embedding-v4 初始化（云端模型）
        if self.embedding_provider == EmbeddingProvider.TEXT_EMBEDDING_V4:
            if not DASHSCOPE_API_KEY:
                raise ValueError("使用 text-embedding-v4 需要配置 DASHSCOPE_API_KEY 或 QWEN3_API_KEY")
            dashscope.api_key = DASHSCOPE_API_KEY
            # 若使用新加坡地域的模型，请取消以下注释
            # dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

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
        注意：使用 query_embeddings 而不是 query_texts，避免 ChromaDB 使用默认的本地 embedding 模型
        
        Args:
            symptoms: 症状描述文本
            top_k: 返回最相关的 top_k 个结果
            min_score: 最小相似度阈值（0-1），距离越小相似度越高，需要转换为相似度后比较
        """
        if not symptoms:
            return []
        try:
            # 先使用配置的 embedding 模型将症状文本向量化
            query_embedding = self.get_embedding([symptoms])[0]
            
            # 使用 query_embeddings 而不是 query_texts，避免触发 ChromaDB 默认的本地模型
            # 增加返回数量，以便后续根据相似度过滤
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k * 2, 20),  # 多查询一些，然后根据相似度过滤
                include=["metadatas", "distances"]
            )
            metadatas = results.get('metadatas') or []
            distances = results.get('distances') or []
            if not metadatas or not distances or not isinstance(metadatas, list) or not isinstance(distances, list):
                return []
            metadatas = metadatas[0] if len(metadatas) > 0 else []
            distances = distances[0] if len(distances) > 0 else []
            
            # ChromaDB 使用余弦距离，范围通常是 0-2
            # 距离越小 = 相似度越高
            # 将距离转换为相似度：similarity = 1 - (distance / 2)，范围 0-1
            # 或者使用更严格的阈值：max_distance = 2 * (1 - min_score)
            max_distance = 2 * (1 - min_score)  # 将相似度阈值转换为最大距离阈值
            
            filtered_results = []
            for meta, dist in zip(metadatas, distances):
                if 'drug_json' in meta and isinstance(meta['drug_json'], str):
                    # 距离越小越相似，所以应该 dist <= max_distance
                    if dist <= max_distance:
                        try:
                            drug_data = json.loads(meta['drug_json'])
                            # 计算相似度用于排序
                            similarity = 1 - (dist / 2) if dist <= 2 else 0
                            filtered_results.append((drug_data, similarity, dist))
                        except json.JSONDecodeError:
                            continue
            
            # 按相似度降序排序，取前 top_k 个
            filtered_results.sort(key=lambda x: x[1], reverse=True)
            return [drug_data for drug_data, _, _ in filtered_results[:top_k]]
            
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
        if self.embedding_provider == EmbeddingProvider.TEXT_EMBEDDING_V4:
            return self.get_text_embedding_v4(texts)
        else:
            return self.get_bge_m3_embedding(texts)

    def get_text_embedding_v4(self, texts: list[str]) -> list:
        """使用 dashscope text-embedding-v4 模型，支持批量"""
        try:
            # dashscope 支持批量输入，可以是字符串或字符串列表
            if len(texts) == 1:
                input_text = texts[0]
            else:
                input_text = texts
            
            resp = dashscope.TextEmbedding.call(
                model="text-embedding-v4",
                input=input_text
            )
            
            if resp.status_code == HTTPStatus.OK:
                # 处理返回结果
                if isinstance(input_text, str):
                    # 单个文本
                    embeddings = [resp.output["embeddings"][0]["embedding"]]
                else:
                    # 批量文本
                    embeddings = [item["embedding"] for item in resp.output["embeddings"]]
                return embeddings
            else:
                error_msg = f"text-embedding-v4 调用失败: status_code={resp.status_code}, message={resp.message}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        except Exception as e:
            logger.error(f"text-embedding-v4 embedding 服务调用失败: {e}")
            raise

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