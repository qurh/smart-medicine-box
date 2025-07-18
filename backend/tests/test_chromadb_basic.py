import chromadb
from chromadb.config import Settings
import json
import pytest

CHROMA_DIR = "app/chroma_db"
COLLECTION_NAME = "medicine_drugs"

@pytest.fixture(scope="module")
def collection():
    client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME)

def test_chromadb_all_drugs(collection):
    results = collection.get()
    ids = results.get('ids')
    metadatas = results.get('metadatas')
    if not ids or not metadatas:
        pytest.skip("ChromaDB中无数据，跳过测试")
    assert isinstance(ids, list)
    assert isinstance(metadatas, list)
    assert len(ids) == len(metadatas)
    assert len(ids) > 0
    for meta in metadatas:
        assert isinstance(meta, dict)
        assert 'drug_json' in meta
        drug = json.loads(meta['drug_json'])
        assert 'name' in drug

def test_chromadb_get_by_id(collection):
    results = collection.get()
    ids = results.get('ids')
    if not ids:
        pytest.skip("ChromaDB中无数据，跳过测试")
    drug_id = ids[0]
    result = collection.get(ids=[drug_id])
    assert 'ids' in result and result['ids'][0] == drug_id

def test_chromadb_search_by_symptom(collection):
    results = collection.get()
    ids = results.get('ids')
    if not ids:
        pytest.skip("ChromaDB中无数据，跳过测试")
    symptom = "发热头痛"
    result = collection.query(query_texts=[symptom], n_results=3)
    assert 'ids' in result
    assert isinstance(result['ids'][0], list) or isinstance(result['ids'], list)
    assert len(result['ids'][0]) <= 3 or len(result['ids']) <= 3 