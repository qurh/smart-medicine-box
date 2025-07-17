# 家庭智能药箱前端（Smart Medicine Box Frontend）项目生成

## 项目定位
基于 Vue3 + Vite + Element Plus + TailwindCSS 的家庭智能药箱前端，支持药品扫码/查询、信息展示、药箱管理、mock数据、接口联调、UI美化、环境配置等功能。

---

## 目录结构建议
```
front/
├── src/
│   ├── pages/           # 页面组件（Home.vue, DrugList.vue 等）
│   ├── components/      # 复用型UI组件（如 DrugCard.vue、DrugForm.vue、Loading.vue、ErrorAlert.vue 等）
│   ├── api/             # API 封装（如 drug.ts，统一管理所有接口请求）
│   ├── stores/          # 状态管理（如 pinia store，药箱、用户等）
│   ├── types/           # TypeScript 类型声明（如 drug.d.ts）
│   ├── utils/           # 工具函数（如格式化、校验等）
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

---

## 代码架构与开发最佳实践
- 页面（pages）只负责页面布局和业务流转，具体UI和交互拆分为复用型组件（components）。
- 业务相关的 API 请求统一封装在 src/api/ 下，便于维护和mock。
- 推荐使用 Pinia 进行全局状态管理，药箱、用户等全局数据放在 src/stores/ 下。
- 所有数据结构、接口响应、表单等类型统一在 src/types/ 下声明，前后端类型强校验。
- 工具函数（如日期格式化、字段映射等）统一放在 src/utils/ 下。
- 组件样式优先用 TailwindCSS，局部细节可用 scoped CSS。
- 路由采用 history 模式，App.vue 仅为路由壳。
- 统一 .gitignore，忽略 node_modules、dist、环境变量、日志等。
- 推荐使用 TypeScript，提升类型安全和开发体验。
- 友好的加载、错误提示，mock数据支持前端独立开发。
- 详细开发文档见 README.md。

---

## 主要功能与要求
1. 首页（Home.vue）：支持药品名称查询，展示药品信息，支持“放入家庭药箱”按钮，保存后跳转药品列表页。
2. 药品列表页（DrugList.vue）：卡片式分块展示药品信息，卡片有圆角、阴影、渐变背景，内容分块排版，支持自动刷新和分页预留。
3. 复用型组件建议：
   - DrugCard.vue：单个药品卡片展示
   - DrugForm.vue：药品录入/编辑表单
   - Loading.vue：加载状态
   - ErrorAlert.vue：错误提示
4. API 请求通过 src/api/ 统一管理，所有接口响应通过 data 字段获取数据，code/msg 用于错误处理。
5. 状态管理通过 Pinia（src/stores/）实现，便于多页面/组件间共享。
6. 类型声明通过 src/types/ 统一管理，接口、表单、药品等类型强校验。
7. 环境变量 `.env` 配置 VITE_API_URL，所有 API 请求通过该变量拼接。
8. 支持 mock 数据，便于前端独立开发和测试。

---

## 主要接口示例（前端请求格式）
- 查询药品信息：`POST /api/scan`，body: `{ "drug_name": "xxx" }`
- 保存药品信息：`POST /api/save-drug-info`，body: `{ ...药品信息... }`
- 获取药箱列表：`GET /api/drug-list`，无参数

---

## 组件化开发建议
- 组件 props/emit 明确，类型强校验，避免隐式依赖。
- 复用型组件拆分粒度适中，UI与业务解耦。
- 组件样式优先 TailwindCSS，局部细节可用 scoped CSS。
- 业务逻辑与视图分离，API、store、utils 不直接耦合到组件。
- 适当使用组合式 API（setup、ref、computed、watch、provide/inject 等）。
- 复杂表单建议用 Element Plus 表单组件，配合类型声明和校验。

---

## 其他最佳实践
- 统一 .gitignore，忽略依赖、dist、环境变量、日志等。
- 代码结构清晰，便于维护和扩展。
- mock数据丰富，便于前端开发和演示。
- 错误处理和提示友好，便于调试。
