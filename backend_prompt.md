# 家庭智能药箱后端（Smart Medicine Box Backend）项目生成 

## 项目定位
基于 FastAPI + Pydantic + LangChain + Qwen3 + Loguru + python-dotenv 的家庭智能药箱后端，采用分层解耦、类型安全、配置灵活、易于测试和扩展的架构，支持药品扫码/查询、信息提取、药箱管理、mock数据、接口联调、配置管理等功能。

---

## 目录结构建议（分层解耦最佳实践）
```
backend/
├── app/
│   ├── main.py              # FastAPI 入口，含CORS、lifespan事件、路由注册、全局异常处理
│   ├── core/                # 核心配置与工具（如 config.py, logger.py, deps.py）
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

## 代码架构与开发最佳实践
- **分层解耦**：路由（routers）、业务（services）、数据模型（models/schemas）、工具（utils）、配置（core）分层清晰，便于维护和扩展。
- **类型安全**：所有接口请求/响应、业务逻辑、数据存储均用 Pydantic 类型强校验。
- **配置灵活**：所有敏感信息、mock开关、API Key等通过 .env 管理，支持多环境（开发、测试、生产）。
- **全局异常处理**：main.py 注册全局异常处理，统一错误响应格式。
- **mock 支持**：mock 数据与真实数据解耦，便于前端开发和接口联调。
- **日志与调试**：Loguru 日志，详细记录请求、异常、关键业务流程。
- **测试友好**：tests 目录下按业务分模块编写测试用例，接口、服务、mock均可单测。
- **启动灵活**：支持命令行和环境变量配置 host/port，采用 lifespan 事件替换 on_event。
- **接口风格统一**：RESTful，所有接口统一 BaseRequest/BaseResponse（code/msg/data结构），便于前端解析。
- **.gitignore 完善**：忽略 venv、__pycache__、日志、环境变量、测试缓存等。

---

## 主要功能与要求
1. 提供药品信息查询、保存、药箱列表等RESTful接口，接口路径分别为 `/api/drug/scan`、`/api/drug/save`、`/api/drug/list`。
2. 所有接口统一请求/响应模型（BaseRequest/BaseResponse，code/msg/data结构），便于前端解析。
3. 药品信息提取 prompt 输出为严格 JSON 格式，便于后端解析。
4. 支持 mock 数据，药箱数据存储在本地 JSON 文件（medicine_box.json），便于前端开发和测试。
5. 配置、API Key、mock开关等通过 .env 文件统一管理，支持多环境（开发、测试、生产）。
6. 启动脚本支持命令行和环境变量配置 host/port，采用 lifespan 事件替换 on_event。
7. 详细的错误提示与日志，便于快速定位问题。
8. 代码结构清晰，易于维护和扩展，便于团队协作。

---

## 主要接口示例（后端接口格式）
- 查询药品信息：`POST /api/drug/scan`，body: `{ "drug_name": "xxx" }`，返回 `{ "code": 0, "msg": "success", "data": { ...药品信息... } }`
- 保存药品信息：`POST /api/drug/save`，body: `{ ...药品信息... }`，返回 `{ "code": 0, "msg": "保存成功", "data": null }`
- 获取药箱列表：`GET /api/drug/list`，返回 `{ "code": 0, "msg": "success", "data": [ ...药品列表... ] }`

---

## 开发建议
- FastAPI + Pydantic 统一接口风格，便于前端解析。
- 路由、业务、模型、工具、配置分层清晰，便于维护和扩展。
- 配置、mock、API Key等通过.env管理。
- mock与真实数据解耦，便于前端独立开发和测试。
- 测试用例建议覆盖接口、服务、mock等关键路径。
- 详细开发文档见 README.md。 