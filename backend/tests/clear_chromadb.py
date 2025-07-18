import chromadb
from chromadb.config import Settings

CHROMA_DIR = "app/chroma_db"
COLLECTION_NAME = "medicine_drugs"

def clear_chromadb():
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    all_ids = collection.get().get('ids', [])
    if all_ids:
        collection.delete(ids=all_ids)
        print(f"已清空 ChromaDB collection: {COLLECTION_NAME}，共删除 {len(all_ids)} 条数据")
    else:
        print(f"ChromaDB collection: {COLLECTION_NAME} 已为空")

if __name__ == "__main__":
    confirm = input(f"确定要清空 ChromaDB collection '{COLLECTION_NAME}' 的所有数据吗？(y/n): ").strip().lower()
    if confirm == 'y':
        clear_chromadb()
    else:
        print("操作已取消")