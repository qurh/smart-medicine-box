# 通用全栈项目初始化说明

## 项目定位
本项目为典型的前后端分离全栈管理系统，支持扫码/查询、信息录入、数据管理、mock数据、接口联调、UI美化、环境配置等功能，适合各类业务场景。

---

## 技术栈
- **前端**：Vue3 + Vite + Element Plus + TailwindCSS + Pinia + TypeScript
- **后端**：FastAPI + Pydantic + Loguru + python-dotenv + pytest（可选AI/大模型/第三方API能力）

---

## 推荐目录结构

### 前端（front/）
```
front/
├── src/
│   ├── pages/           # 页面组件，业务功能命名（如 XxxPage.vue）
│   ├── components/      # 复用型UI组件，功能/通用性命名（如 XxxCard.vue、XxxForm.vue）
│   ├── api/             # API 封装，领域相关命名（如 user.ts、order.ts）
│   ├── stores/          # 状态管理，Pinia store，领域命名（如 userStore.ts）
│   ├── types/           # TypeScript 类型声明，领域/用途命名（如 user.d.ts、api.d.ts）
│   ├── utils/           # 工具函数，功能命名（如 date.ts、format.ts）
│   ├── App.vue          # 路由壳组件
│   ├── main.ts          # 入口文件
│   └── index.css        # 全局样式
├── public/
├── .env                 # 环境变量（如 VITE_API_URL）
├── package.json
├── tailwind.config.js
├── postcss.config.cjs
└── ...
```

### 后端（backend/）
```
backend/
├── app/
│   ├── main.py              # FastAPI 入口，含CORS、lifespan事件、路由注册、全局异常处理
│   ├── core/                # 配置与日志（如 config.py, logger.py）
│   ├── routers/             # 路由分组（如 user.py、drug.py）
│   ├── models/              # Pydantic 数据模型（如 user.py、order.py）
│   ├── schemas/             # 请求/响应模型（如 base_request.py, base_response.py, requests.py）
│   ├── services/            # 业务逻辑（如 user_service.py, order_service.py, mock_service.py）
│   ├── utils/               # 工具函数（如 file_io.py, date_util.py）
│   └── prompts/             # LLM prompt 模板
├── requirements.txt
├── .env                    # 环境变量
├── tests/                  # 测试用例（如 test_user.py）
└── ...
```

---

## 主要功能与最佳实践
- **分层解耦**：前后端均采用页面/组件/服务/工具/类型/配置分层，单一职责，便于维护和扩展。
- **类型安全**：前端 TypeScript、后端 Pydantic 全面类型校验。
- **mock 支持**：前后端均支持 mock 数据，便于独立开发和测试。
- **RESTful接口，统一请求/响应结构**：所有接口统一 BaseRequest/BaseResponse（code/msg/data结构），便于联调和前端解析。
- **全局异常处理与详细日志**：后端 main.py 注册全局异常处理，日志详细，便于排查。
- **多环境配置**：.env 管理多环境，前端 VITE_API_URL，后端支持多种配置。
- **组件化开发**：props/emit 明确，类型强校验，业务逻辑与视图分离，API/store/utils 不直接耦合到组件。
- **自动化测试**：后端 pytest，前端建议配合 Vitest/Jest。
- **接口文档自动生成**：后端推荐 /docs。
- **代码结构清晰，便于团队协作和扩展。**

---

## 虚拟开发环境建议

### 前端
- 推荐使用 nvm（Node Version Manager）或 Volta 管理 Node.js 版本，确保团队环境一致。
- 安装 nvm（Windows 推荐 nvm-windows）或 Volta，参考官方文档。
- 切换到项目推荐 Node.js 版本（如 18.x）：
  ```bash
  nvm install 18
  nvm use 18
  # 或
  volta install node@18
  ```
- 然后再进行依赖安装和开发运行。

### 后端
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
### 前端
1. 安装依赖
   ```bash
   npm install
   ```
2. 配置环境变量（.env）
   - VITE_API_URL=http://localhost:8000
3. 启动开发服务
   ```bash
   npm run dev
   ```

### 后端
1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 配置环境变量（.env）
3. 启动服务
   ```bash
   uvicorn main:app --reload
   # 或
   python main.py --env .env --host 0.0.0.0 --port 8000
   ```

---

## 主要接口示例（可根据业务自定义）
- 查询信息：`POST /api/entity/scan`，body: `{ "name": "xxx" }`
- 保存信息：`POST /api/entity/save`，body: `{ ...信息... }`
- 获取列表：`GET /api/entity/list`
- 所有接口响应结构：`{ "code": 0, "msg": "success", "data": ... }`

---

## 其他说明
- 详细开发文档见前后端 README.md。
- 代码结构清晰，便于维护和扩展。
- mock与真实数据解耦，便于前后端独立开发和接口联调。
- 错误处理和提示友好，便于调试。
- 推荐接口文档自动生成（/docs）。
- 代码注释和类型提示齐全，便于团队协作。
