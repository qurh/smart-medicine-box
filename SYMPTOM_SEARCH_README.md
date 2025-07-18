# 症状查询功能说明

## 功能概述

新增的症状查询功能允许用户通过描述症状来查找家庭药箱中的相关药品，使用向量化检索技术提供智能匹配。

## 后端实现

### 1. 新增依赖

在 `backend/requirements.txt` 中添加了以下依赖：
```
sentence-transformers  # 用于文本向量化
numpy                 # 数值计算
scikit-learn         # 相似度计算
```

### 2. 核心服务

**文件**: `backend/app/services/vector_search_service.py`

- 使用 `paraphrase-multilingual-MiniLM-L12-v2` 模型进行中文文本向量化
- 对药箱中的每个药品生成向量嵌入（组合药品名称、适应症、用法用量等信息）
- 通过余弦相似度计算症状与药品的相关性
- 支持相似度阈值过滤，确保结果质量

### 3. API接口

**新增接口**: `POST /api/drug/search-by-symptoms`

**请求参数**:
```json
{
  "symptoms": "头痛发烧",
  "top_k": 5
}
```

**响应格式**:
```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {
      "name": "布洛芬",
      "indications": "用于缓解轻至中度疼痛",
      "similarity_score": 0.85,
      // ... 其他药品信息
    }
  ]
}
```

### 4. 数据更新机制

- 当添加新药品到药箱时，自动刷新向量嵌入
- 确保搜索结果始终基于最新的药箱数据

## 前端实现

### 1. 新增页面

**症状查询页面**: `front/src/pages/SymptomSearch.vue`
- 提供症状输入框和常见症状标签
- 支持详细症状描述
- 友好的用户界面和错误提示

**查询结果页面**: `front/src/pages/SymptomResults.vue`
- 复用 `DrugCard` 组件展示结果
- 支持分页显示
- 显示相似度分数
- 提供返回和重新查询功能

### 2. API封装

在 `front/src/api/drug.ts` 中新增：
```typescript
export async function searchDrugsBySymptoms(symptoms: string, topK: number = 5): Promise<Drug[]>
```

### 3. 路由配置

在 `front/src/main.ts` 中添加路由：
```typescript
{ path: '/symptom-search', name: 'SymptomSearch', component: SymptomSearch },
{ path: '/symptom-results', name: 'SymptomResults', component: SymptomResults }
```

### 4. 首页导航

更新首页 `front/src/pages/Home.vue`，添加功能导航卡片：
- 症状查询入口
- 药箱管理入口
- 药品扫描入口

## 使用方法

### 1. 安装依赖

**后端**:
```bash
cd backend
pip install -r requirements.txt
```

**前端**:
```bash
cd front
npm install
```

### 2. 启动服务

**后端**:
```bash
cd backend
python main.py
```

**前端**:
```bash
cd front
npm run dev
```

### 3. 使用流程

1. 访问首页，点击"症状查询"卡片
2. 在症状查询页面输入症状描述（如"头痛发烧"）
3. 点击"查询相关药品"按钮
4. 查看匹配的药品列表和相似度分数
5. 可以点击药品卡片查看详细信息

### 4. 测试功能

运行测试脚本：
```bash
python test_symptom_search.py
```

## 技术特点

### 1. 智能匹配
- 使用预训练的中文多语言模型
- 支持语义相似度计算
- 考虑药品名称、适应症、用法等多维度信息

### 2. 用户体验
- 提供常见症状标签快速选择
- 支持详细症状描述
- 显示相似度分数，帮助用户判断相关性

### 3. 性能优化
- 向量嵌入预计算，查询响应快速
- 相似度阈值过滤，确保结果质量
- 支持分页显示，处理大量结果

### 4. 可扩展性
- 模块化设计，易于维护和扩展
- 支持不同的向量化模型
- 可配置相似度算法和阈值

## 注意事项

1. **首次启动**: 向量化模型首次加载可能需要一些时间
2. **内存使用**: 向量嵌入会占用一定内存，建议在服务器上配置足够内存
3. **模型下载**: 首次使用时会自动下载预训练模型，需要网络连接
4. **数据质量**: 药品信息的完整性和准确性直接影响查询效果

## 后续优化建议

1. **缓存机制**: 添加向量嵌入的缓存，提高启动速度
2. **批量更新**: 支持批量药品更新时的向量重建
3. **用户反馈**: 收集用户对查询结果的反馈，优化算法
4. **多语言支持**: 扩展支持更多语言的症状描述
5. **个性化推荐**: 基于用户历史查询记录提供个性化推荐 