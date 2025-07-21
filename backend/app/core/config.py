import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
QWEN3_API_KEY = os.getenv("QWEN3_API_KEY", "")
MEDICINE_BOX_FILE = BASE_DIR / "medicine_box.json"

# chroma 持久化目录，默认 backend/chroma_db
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", BASE_DIR / "chroma_db")).resolve()
print(f"[启动] CHROMA_PERSIST_DIR: {CHROMA_PERSIST_DIR}")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "medicine_drugs")

# embedding 相关配置
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "cloud_bge_m3")
EMBEDDING_MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", str(BASE_DIR / "models" / "paraphrase-multilingual-MiniLM-L12-v2"))

class Settings:
    EMBEDDING_PROVIDER = EMBEDDING_PROVIDER
    EMBEDDING_MODEL_PATH = EMBEDDING_MODEL_PATH

def get_settings():
    return Settings