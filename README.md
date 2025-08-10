# 家庭智能药箱管理系统（Smart Medicine Box）

一个基于 Vue3 + FastAPI 的智能家庭药箱管理系统，支持药品扫码查询、症状智能检索、药箱管理等功能。

## 🚀 项目特色

- **智能检索**：基于向量化技术的症状-药品智能匹配
- **双模式支持**：Mock数据模式（开发/演示）+ 正式环境模式（生产/联调）
- **现代化架构**：前后端分离，类型安全，组件化开发
- **灵活配置**：支持云端/本地 embedding 模型切换
- **完整功能**：药品管理、症状查询、药箱维护等全流程

## 🏗️ 技术架构

### 后端技术栈
- **框架**：FastAPI + Pydantic v2
- **AI能力**：LangChain + Qwen3（可选）
- **向量数据库**：ChromaDB（本地持久化）
- **Embedding模型**：支持云端 bge-m3 和本地 SentenceTransformer
- **日志**：Loguru
- **配置**：python-dotenv
- **测试**：pytest

### 前端技术栈
- **框架**：Vue3（Composition API）
- **构建工具**：Vite
- **语言**：TypeScript
- **UI组件**：Element Plus
- **样式框架**：TailwindCSS
- **状态管理**：Pinia
- **代码规范**：ESLint + Prettier

## 📁 项目结构

```
smart-medicine-box/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── core/           # 配置与日志
│   │   ├── models/         # Pydantic 数据模型
│   │   ├── routers/        # API 路由
│   │   ├── schemas/        # 请求/响应模型
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── prompts/        # LLM prompt 模板
│   ├── tests/              # 测试用例
│   ├── main.py             # 服务入口
│   ├── requirements.txt    # Python 依赖
│   └── README.md           # 后端详细文档
├── front/                   # 前端应用
│   ├── src/
│   │   ├── pages/          # 页面组件
│   │   ├── components/     # 复用型UI组件
│   │   ├── api/            # API 封装
│   │   ├── stores/         # 状态管理
│   │   ├── types/          # TypeScript 类型声明
│   │   └── utils/          # 工具函数
│   ├── package.json        # Node.js 依赖
│   └── README.md           # 前端详细文档
├── .gitignore              # Git 忽略文件
└── README.md               # 项目总览（本文件）
```

## 🎯 核心功能

### 1. 药品管理
- **药品扫描**：输入药品名称，智能解析药品信息
- **药箱管理**：添加、查看、管理家庭药箱中的药品
- **信息展示**：药品详细信息、用法用量、适应症等

### 2. 症状智能检索 🆕
- **症状输入**：支持自然语言描述症状
- **智能匹配**：基于向量化技术的药品-症状相关性计算
- **结果排序**：按相似度分数排序，提供最相关药品

### 3. 双模式支持
- **Mock模式**：本地JSON数据，便于前端开发和演示
- **正式模式**：ChromaDB向量数据库，支持智能检索

## 🚀 快速开始

### 环境要求
- **Python**: 3.8+
- **Node.js**: 18+
- **推荐**: 使用虚拟环境管理工具（Python venv/conda, Node.js nvm/Volta）

### 1. 克隆项目
```bash
git clone <repository-url>
cd smart-medicine-box
```

### 2. 后端设置
```bash
cd backend

# 创建虚拟环境
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量

# 启动服务
python main.py
# 或
uvicorn main:app --reload
```

### 3. 前端设置
```bash
cd front

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 VITE_API_URL

# 启动开发服务
npm run dev
```

### 4. 访问应用
- **前端**: http://localhost:5173
- **后端API文档**: http://localhost:8000/docs

## ⚙️ 配置说明

### 后端配置（.env）
```env
# Mock模式开关
USE_MOCK_DATA=true

# Embedding模型配置
EMBEDDING_PROVIDER=cloud_bge_m3  # 或 local_model
EMBEDDING_MODEL_PATH=path/to/local/model  # 本地模型路径

# API密钥（如需要）
QWEN3_API_KEY=your_api_key
```

### 前端配置（.env）
```env
# API服务地址
VITE_API_URL=http://localhost:8000
```

## 🔧 开发指南

### 后端开发
- **分层架构**：路由、服务、模型、工具分层清晰
- **类型安全**：Pydantic v2 强类型校验
- **Mock支持**：本地JSON数据，便于前端开发
- **向量检索**：支持云端/本地 embedding 模型

### 前端开发
- **组件化**：页面只负责布局，UI拆分为复用组件
- **状态管理**：Pinia 统一状态管理
- **类型安全**：TypeScript 强类型支持
- **API封装**：统一接口管理，支持Mock切换

## 🧪 测试

### 后端测试
```bash
cd backend
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_symptom_search.py
```

### 前端测试
```bash
cd front
npm run test
```

## 📚 API 接口

### 核心接口
- `POST /api/drug/scan` - 查询药品信息
- `POST /api/drug/save` - 保存药品信息
- `GET /api/drug/list` - 获取药箱列表
- `POST /api/drug/search-by-symptoms` - 症状智能检索

### 响应格式
所有接口统一使用 BaseResponse 格式：
```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

## 🔄 Mock与正式环境切换

### Mock模式（开发/演示）
- 设置 `USE_MOCK_DATA=true`
- 所有数据来自本地 `medicine_box.json`
- 症状检索返回随机药品

### 正式模式（生产/联调）
- 设置 `USE_MOCK_DATA=false`
- 数据存储在 ChromaDB 向量数据库
- 症状检索基于真实向量相似度计算

## 🌟 特色功能

### 症状智能检索
- 使用预训练中文多语言模型
- 支持语义相似度计算
- 考虑药品名称、适应症、用法等多维度信息
- 相似度阈值过滤，确保结果质量

### 向量化存储
- ChromaDB 本地持久化
- 支持云端/本地 embedding 模型
- 药品信息向量化，支持智能检索

## 📖 详细文档

- [后端开发文档](backend/README.md) - 后端架构、API、配置等详细信息
- [前端开发文档](front/README.md) - 前端组件、状态管理、开发规范等
- [症状查询功能说明](症状查询功能说明.md) - 智能检索功能详细说明

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 参与讨论

---

**注意**: 首次启动时，向量化模型下载可能需要一些时间，请确保网络连接正常。 