# 家庭智能药箱后端（Python FastAPI）

本项目为家庭智能药箱管理系统后端，采用 FastAPI + Pydantic + Loguru + python-dotenv + pytest，分层解耦、类型安全、配置灵活、易于测试和扩展，支持药品扫码/查询、信息提取、药箱管理、mock数据、接口联调、配置管理等功能。

---

## 技术栈
- FastAPI（高性能 Web 框架）
- Pydantic v2（类型安全与数据校验，所有 dict() 已升级为 model_dump()）
- Loguru（日志管理）
- python-dotenv（多环境配置）
- pytest（单元测试）
- LangChain + Qwen3（大模型/AI能力，按需可选）
- Chroma（本地向量数据库，药品主存储与智能检索）

---

## 目录结构
```
backend/
├── app/
│   ├── main.py              # FastAPI 入口，含CORS、lifespan事件、路由注册、全局异常处理
│   ├── core/                # 配置与日志（如 config.py, logger.py）
│   ├── routers/             # 路由分组（如 drug.py）
│   ├── models/              # Pydantic 数据模型（如 drug.py）
│   ├── schemas/             # 请求/响应模型（如 base_request.py, base_response.py, requests.py）
│   ├── services/            # 业务逻辑（如 drug_info_process.py, medicine_box_service.py, mock_service.py, vector_search_service.py）
│   ├── utils/               # 工具函数（如 file_io.py, field_map.py）
│   └── prompts/             # LLM prompt 模板
├── medicine_box.json        # 药箱mock数据（仅mock模式用）
├── requirements.txt
├── .env                    # 环境变量
├── tests/                  # 测试用例（如 test_scan.py）
└── ...
```

---

## 数据存储与mock机制

### 1. 主存储
- **正式环境**：所有药品数据主存储于 Chroma 向量数据库，支持智能检索和全量列表。
- **mock模式**：通过 `.env` 设置 `USE_MOCK_DATA=true`，所有药品数据仅存储于本地 `medicine_box.json`，便于前端开发和演示。

### 2. mock/正式切换
- 通过 `.env` 文件或环境变量 `USE_MOCK_DATA` 控制：
  - `USE_MOCK_DATA=true`：所有读写均走本地 JSON 文件，所有智能检索接口返回 mock 数据。
  - `USE_MOCK_DATA=false`：所有读写均走 Chroma 向量数据库，智能检索为真实 LLM+向量检索。

---

## 主要接口说明

### 1. 查询药品信息
- `POST /api/drug/scan`，body: `{ "drug_name": "xxx" }`
- mock模式：返回本地mock药品信息
- 正式环境：调用大模型解析药品信息

### 2. 保存药品信息
- `POST /api/drug/save`，body: `{ ...药品信息... }`
- mock模式：保存到本地 `medicine_box.json`，新药品插入到头部
- 正式环境：保存到 Chroma 向量数据库（主治功效字段向量化，完整信息存为元数据）

### 3. 获取药箱列表
- `GET /api/drug/list`
- mock模式：返回本地 `medicine_box.json` 全部药品
- 正式环境：返回 Chroma 向量数据库中所有药品元数据

### 4. 症状智能检索
- `POST /api/drug/search-by-symptoms`，body: `{ "symptoms": "xxx", "top_k": 5 }`
- mock模式：从本地 `medicine_box.json` 随机抽取 top_k 个药品返回
- 正式环境：症状文本向量化后在 Chroma 检索最相关药品

---

## mock与正式环境切换

- `.env` 示例：
  ```env
  USE_MOCK_DATA=true  # 开启mock，所有接口走本地JSON
  # USE_MOCK_DATA=false  # 关闭mock，所有接口走向量数据库
  ```
- 推荐开发/演示时用mock，生产/联调时用正式环境

---

## Pydantic v2 升级说明
- 所有 `.dict()` 已替换为 `.model_dump()`，`.json()` 替换为 `.model_dump_json()`，完全兼容Pydantic v2。
- 代码中如需序列化/反序列化Pydantic模型，请统一用 `model_dump()`/`model_dump_json()`。

---

## 其他说明
- mock数据文件 `medicine_box.json` 可手动编辑，便于前端开发和演示。
- 智能检索、药品列表等接口均支持mock与正式切换，便于全流程开发。
- 详细开发文档见本项目及前端 README.md。
- 代码结构清晰，便于维护和扩展。
- 推荐接口文档自动生成（/docs）。
- 代码注释和类型提示齐全，便于团队协作。
