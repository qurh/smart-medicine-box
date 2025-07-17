# 家庭智能药箱后端（Python FastAPI）

本项目为家庭智能药箱管理系统后端，采用 FastAPI + Pydantic + Loguru + python-dotenv + pytest，分层解耦、类型安全、配置灵活、易于测试和扩展，支持药品扫码/查询、信息提取、药箱管理、mock数据、接口联调、配置管理等功能。

---

## 技术栈
- FastAPI（高性能 Web 框架）
- Pydantic（类型安全与数据校验）
- Loguru（日志管理）
- python-dotenv（多环境配置）
- pytest（单元测试）
- LangChain + Qwen3（大模型/AI能力，按需可选）

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
│   ├── services/            # 业务逻辑（如 drug_info_process.py, medicine_box_service.py, mock_service.py）
│   ├── utils/               # 工具函数（如 file_io.py, field_map.py）
│   └── prompts/             # LLM prompt 模板
├── medicine_box.json        # 药箱数据（支持mock）
├── requirements.txt
├── .env                    # 环境变量
├── tests/                  # 测试用例（如 test_scan.py）
└── ...
```

---

## 主要功能
- 药品信息提取（支持大模型/LLM和mock）
- 药品保存与药箱管理（本地JSON）
- RESTful接口，统一请求/响应结构
- mock数据支持，便于前端开发和测试
- 全局异常处理与详细日志
- 多环境配置与灵活启动
- 分层解耦，单一职责，便于维护和扩展
- 类型安全，Pydantic 全面校验

---

## 虚拟开发环境建议
- 强烈建议使用 Python 虚拟环境（venv 或 conda）隔离依赖，避免全局污染。
- 创建并激活虚拟环境（以 venv 为例）：
  ```bash
  python -m venv venv
  # Windows
  .\venv\Scripts\activate
  # macOS/Linux
  source venv/bin/activate
  ```
- 然后再进行依赖安装和开发运行。

## 开发与运行
1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 配置环境变量（.env）
   - QWEN3_API_KEY, USE_MOCK_DATA, ...
3. 启动服务
   ```bash
   uvicorn main:app --reload
   # 或
   python main.py --env .env --host 0.0.0.0 --port 8000
   ```
4. 访问接口文档
   - http://localhost:8000/docs

---

## 测试
- 测试用例位于 `tests/` 目录
- 运行全部测试：
  ```bash
  pytest tests/
  ```

---

## 主要接口示例
- 查询药品信息：`POST /api/drug/scan`，body: `{ "drug_name": "xxx" }`
- 保存药品信息：`POST /api/drug/save`，body: `{ ...药品信息... }`
- 获取药箱列表：`GET /api/drug/list`
- 所有接口响应结构：`{ "code": 0, "msg": "success", "data": ... }`

---

## 其他说明
- 详细开发文档见本项目及前端 README.md。
- 代码结构清晰，便于维护和扩展。
- mock与真实数据解耦，便于前端独立开发和接口联调。
- 错误处理和提示友好，便于调试。
- 推荐接口文档自动生成（/docs）。
- 代码注释和类型提示齐全，便于团队协作。
