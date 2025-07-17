# 家庭智能药箱前端（Vue3 + Vite + TypeScript）

本项目为家庭智能药箱管理系统前端，采用 Vue3 + Vite + TypeScript + Element Plus + TailwindCSS + Pinia，支持药品扫码/查询、信息展示、药箱管理、mock数据、接口联调、UI美化、环境配置等功能。

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
│   ├── pages/           # 页面组件，业务功能命名（如 Home.vue, DrugList.vue）
│   ├── components/      # 复用型UI组件（如 DrugCard.vue、DrugForm.vue、Loading.vue、ErrorAlert.vue）
│   ├── api/             # API 封装（如 drug.ts）
│   ├── stores/          # 状态管理（如 medicineBox.ts）
│   ├── types/           # TypeScript 类型声明（如 drug.d.ts）
│   ├── utils/           # 工具函数（如 format.ts）
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

## 主要功能
- 首页支持药品名称查询，展示药品信息，支持“放入家庭药箱”按钮，保存后跳转药品列表页。
- 药品列表页卡片式分块展示药品信息，卡片有圆角、阴影、渐变背景，内容分块排版，支持自动刷新和分页预留。
- 组件化开发，props/emit 明确，类型强校验，业务逻辑与视图分离。
- API 请求统一封装，接口联调便捷，支持 mock 数据。
- 全局状态管理用 Pinia，类型声明集中管理。
- 友好的加载、错误提示，mock数据支持前端独立开发。
- 支持多环境配置，接口地址通过 VITE_API_URL 环境变量管理。

---

## 虚拟开发环境建议
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

## 开发与运行
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
4. 访问前端页面
   - http://localhost:5173 或实际端口

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

## mock与接口联调
- 支持 mock 数据，便于前端独立开发和测试。
- 与后端接口联调采用统一的 BaseResponse（code/msg/data结构），前端已适配。

---

## 其他
- 详细开发文档见本项目及后端 README.md。
- 代码结构清晰，便于维护和扩展。
- 错误处理和提示友好，便于调试。
