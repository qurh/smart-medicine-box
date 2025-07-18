# 家庭智能药箱前端（Vue3 + Vite + TypeScript）

本项目为家庭智能药箱管理系统前端，采用 Vue3 + Vite + TypeScript + Element Plus + TailwindCSS + Pinia，支持药品扫码/查询、症状智能检索、信息展示、药箱管理、mock数据、接口联调、UI美化、环境配置等功能。

---

## 技术栈
- Vue3（Composition API）
- Vite（极速开发与构建）
- TypeScript（类型安全）
- Element Plus（UI 组件库）
- TailwindCSS（原子化 CSS 框架）
- Pinia（状态管理）
- ESlint + Prettier（代码规范）

---

## 目录结构
```
front/
├── src/
│   ├── pages/           # 页面组件（Home.vue, DrugList.vue, DrugScan.vue, SymptomSearch.vue, SymptomResults.vue）
│   ├── components/      # 复用型UI组件（DrugCard.vue、DrugForm.vue、Loading.vue、ErrorAlert.vue）
│   ├── api/             # API 封装（drug.ts）
│   ├── stores/          # 状态管理（medicineBox.ts）
│   ├── types/           # TypeScript 类型声明（drug.d.ts）
│   ├── utils/           # 工具函数（format.ts）
│   ├── App.vue          # 路由壳组件
│   ├── main.ts          # 入口文件
│   └── index.css        # 全局样式
├── public/
├── .env                 # 环境变量（如 VITE_PROXY_TARGET）
├── package.json
├── tailwind.config.js
├── postcss.config.cjs
└── ...
```

---

## 主要页面与功能
- **首页（Home.vue）**：卡片式导航，支持跳转到症状查询、药箱管理、药品扫描等核心功能。
- **症状查询（SymptomSearch.vue + SymptomResults.vue）**：输入症状，智能检索相关药品，支持mock和真实检索切换。
- **药品扫描（DrugScan.vue）**：输入药品名称，查询药品信息并可放入家庭药箱。
- **药品列表（DrugList.vue）**：卡片式展示药箱内所有药品，支持分页、自动刷新。
- **复用型组件**：
  - DrugCard.vue：单个药品卡片展示
  - DrugForm.vue：药品录入/编辑表单
  - Loading.vue：加载状态
  - ErrorAlert.vue：错误提示

---

## 组件化开发最佳实践
- 页面只负责布局和业务流转，具体UI和交互拆分为复用型组件。
- 组件 props/emit 明确，类型强校验，避免隐式依赖。
- 业务逻辑与视图分离，API、store、utils 不直接耦合到组件。
- API 请求统一封装在 src/api/ 下，便于维护和 mock。
- 全局状态管理用 Pinia，类型声明集中管理。
- 工具函数统一放在 src/utils/ 下。
- 组件样式优先 TailwindCSS，局部细节可用 scoped CSS。
- 推荐 TypeScript，提升类型安全和开发体验。

---

## mock机制与接口联调
- 支持 mock 数据，便于前端独立开发和测试。
- 后端通过 USE_MOCK_DATA 环境变量切换 mock/正式模式：
  - mock模式：所有接口数据来自本地 JSON 文件，症状检索为随机药品。
  - 正式模式：所有接口数据来自后端向量数据库，症状检索为智能相似度检索。
- 前端无需修改代码即可适配 mock/正式切换。
- 所有接口响应结构统一为 BaseResponse（code/msg/data结构），前端已适配。

---

## 虚拟开发环境建议
- 推荐使用 nvm（Node Version Manager）或 Volta 管理 Node.js 版本，确保团队环境一致。
- 安装 nvm（Windows 推荐 nvm-windows）或 Volta，参考官方文档。
- 切换到项目推荐 Node.js 版本（如 22.x）：
  ```bash
  nvm install 22
  nvm use 22
  # 或
  volta install node@22
  ```
- 然后再进行依赖安装和开发运行。

---

## 开发与运行
1. 安装依赖
   ```bash
   npm install
   ```
2. 配置环境变量（.env）
   - VITE_API_URL=http://localhost:8000
   - .env 可从 .env.example 拷贝后重命名为 .env
3. 启动开发服务
   ```bash
   npm run dev
   ```
4. 访问前端页面
   - http://localhost:5173 或实际端口

---

## 其他
- 代码结构清晰，便于维护和扩展。
- 错误处理和提示友好，便于调试。
- 支持多环境配置，接口地址通过 VITE_PROXY_TARGET 环境变量管理。
