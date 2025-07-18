import chromadb
from chromadb.config import Settings
import json

# 配置与collection名需与主项目一致
CHROMA_DIR = "app/chroma_db"
COLLECTION_NAME = "medicine_drugs"

def print_all_drugs():
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    results = collection.get()
    metadatas = results.get('metadatas')
    if not metadatas:
        print("无数据")
        return
    print(f"共{len(results['ids'])}条药品")
    for i, meta in enumerate(metadatas):
        drug = json.loads(meta['drug_json']) if isinstance(meta, dict) and 'drug_json' in meta and isinstance(meta['drug_json'], str) else meta
        print(f"[{i+1}] {drug.get('name', '-')}")
        print(json.dumps(drug, ensure_ascii=False, indent=2))
        print('-'*40)

def get_drug_by_id(drug_id):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    result = collection.get(ids=[drug_id])
    print(json.dumps(result, ensure_ascii=False, indent=2))

def search_by_symptom(symptom, top_k=5):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    result = collection.query(query_texts=[symptom], n_results=top_k)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def export_all_drugs_to_json(outfile="all_drugs_export.json"):
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    results = collection.get()
    metadatas = results.get('metadatas')
    if not metadatas:
        print("无数据")
        return
    all_drugs = [json.loads(meta['drug_json']) for meta in metadatas if isinstance(meta, dict) and 'drug_json' in meta and isinstance(meta['drug_json'], str)]
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(all_drugs, f, ensure_ascii=False, indent=2)
    print(f"已导出 {len(all_drugs)} 条药品到 {outfile}")

if __name__ == "__main__":
    print("ChromaDB 测试工具")
    print("1. 打印全部药品\n2. 按id查药品\n3. 症状相似度查找\n4. 导出全部药品\n")
    op = input("选择操作(1/2/3/4): ").strip()
    if op == "1":
        print_all_drugs()
    elif op == "2":
        did = input("输入药品名称(唯一id): ").strip()
        get_drug_by_id(did)
    elif op == "3":
        symptom = input("输入症状描述: ").strip()
        search_by_symptom(symptom)
    elif op == "4":
        export_all_drugs_to_json()
    else:
        print("无效选择") 