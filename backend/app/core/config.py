import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
QWEN3_API_KEY = os.getenv("QWEN3_API_KEY", "")
MEDICINE_BOX_FILE = BASE_DIR / "medicine_box.json"

# 向量模型配置
VECTOR_MODEL_NAME = os.getenv("VECTOR_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
# chroma 持久化目录，默认 backend/chroma_db
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", BASE_DIR / "chroma_db")).resolve()
print(f"[启动] CHROMA_PERSIST_DIR: {CHROMA_PERSIST_DIR}")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "medicine_drugs")