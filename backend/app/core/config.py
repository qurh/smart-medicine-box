import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
QWEN3_API_KEY = os.getenv("QWEN3_API_KEY", "")
MEDICINE_BOX_FILE = os.path.join(BASE_DIR, "medicine_box.json")

# 向量模型配置
VECTOR_MODEL_NAME = os.getenv("VECTOR_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
# chroma 持久化目录
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", os.path.join(BASE_DIR, "chroma_db"))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "medicine_drugs")