import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.core.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
from app.models.drug import Drug
from app.services.vector_search_service import VectorSearchService

MEDICINE_BOX_FILE = Path(__file__).resolve().parent.parent / "medicine_box.json"

def batch_import():
    if not MEDICINE_BOX_FILE.exists():
        print(f"未找到数据文件: {MEDICINE_BOX_FILE}")
        sys.exit(1)

    with open(MEDICINE_BOX_FILE, "r", encoding="utf-8") as f:
        drugs = json.load(f)

    if not isinstance(drugs, list):
        print("medicine_box.json 格式错误，应为药品列表")
        sys.exit(1)

    print(f"共读取到 {len(drugs)} 条药品数据，开始批量导入向量数据库...")

    vector_service = VectorSearchService()
    count = 0
    for d in drugs:
        try:
            drug = Drug(**d)
            vector_service.add_drug_embedding(drug)
            count += 1
        except Exception as e:
            print(f"导入失败: {d.get('name', '-')}, 错误: {e}")

    print(f"已成功导入 {count} 条药品到 ChromaDB ({CHROMA_COLLECTION_NAME})，持久化目录: {CHROMA_PERSIST_DIR}")

if __name__ == "__main__":
    print("批量导入药品数据到 ChromaDB 脚本启动...")
    try:
        batch_import()
    except Exception as e:
        print(f"批量导入过程中发生异常: {e}")
        sys.exit(1) 