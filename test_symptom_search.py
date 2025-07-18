#!/usr/bin/env python3
"""
症状查询功能测试脚本
"""

import requests
import json

# 后端服务地址
BASE_URL = "http://localhost:8000"

def test_symptom_search():
    """测试症状查询功能"""
    
    # 测试症状查询
    symptoms = "头痛发烧"
    print(f"测试症状查询: {symptoms}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/drug/search-by-symptoms",
            json={"symptoms": symptoms, "top_k": 5},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"查询成功: {result}")
            
            if result.get("code") == 0:
                data = result.get("data", [])
                print(f"找到 {len(data)} 个相关药品:")
                for i, drug in enumerate(data, 1):
                    similarity = drug.get("similarity_score", 0)
                    print(f"  {i}. {drug.get('name', '未知')} (相似度: {similarity:.3f})")
            else:
                print(f"查询失败: {result.get('msg')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"请求失败: {e}")

def test_drug_list():
    """测试药品列表接口"""
    print("\n测试药品列表接口:")
    
    try:
        response = requests.get(f"{BASE_URL}/api/drug/list")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                data = result.get("data", [])
                print(f"药箱中共有 {len(data)} 个药品")
                for drug in data:
                    print(f"  - {drug.get('name', '未知')}")
            else:
                print(f"获取失败: {result.get('msg')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    print("=== 症状查询功能测试 ===\n")
    
    # 测试药品列表
    test_drug_list()
    
    # 测试症状查询
    test_symptom_search()
    
    print("\n=== 测试完成 ===") 