import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_drug_scan():
    response = client.post("/api/drug/scan", json={"drug_name": "阿莫西林"})
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "name" in data["data"]
    assert data["data"]["name"].startswith("阿莫西林")

def test_drug_save_and_list():
    # 先保存一条药品
    drug = {
        "name": "测试药品",
        "indications": "测试主治",
        "usage": "测试用法",
        "contraindications": "测试禁忌",
        "precautions": "测试注意",
        "category": "测试类别"
    }
    save_resp = client.post("/api/drug/save", json=drug)
    assert save_resp.status_code == 200
    save_data = save_resp.json()
    assert save_data["code"] == 0
    # 获取药品列表
    list_resp = client.get("/api/drug/list")
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert list_data["code"] == 0
    assert any(item["name"] == "测试药品" for item in list_data["data"]) 