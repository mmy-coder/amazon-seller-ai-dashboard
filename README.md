# Amazon Seller AI Dashboard

## 📊 项目定位

Amazon 跨境电商 AI 数据后台 —— 一个用于学习、作品集展示、面试展示的全栈 Web 应用。

模拟 Amazon 卖家在日常运营中会用到的数据分析后台，涵盖商品管理、竞品分析、利润测算、AI 评论分析和 Listing 优化等核心模块。

**这不是商业系统，而是学习项目** —— 帮助理解跨境电商的数据决策逻辑和全栈 Web 开发流程。

---

## 🚀 功能模块

| 模块 | 功能 | 说明 |
|------|------|------|
| 📊 **Dashboard** | 运营数据看板 | 商品总数、竞品数、平均利润率、库存预警、风险统计、图表 |
| 📦 **Products** | 商品管理 | 商品 CRUD、状态管理、库存跟踪 |
| 🔍 **Competitors** | 竞品分析 | 竞品 CRUD、卖点分析、弱点分析、差异化机会 |
| 💰 **Profit Calculator** | 利润计算器 | 成本输入 → 利润/利润率/保本售价/风险等级计算 |
| 🤖 **AI Reviews** | AI 评论分析 | 粘贴评论 → AI 提取痛点/好评/差评/改进建议/卖点 |
| 📋 **AI Listing** | AI Listing 优化 | 输入产品信息 → AI 生成标题/五点描述/关键词/产品描述 |

---

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | **FastAPI** (Python) |
| 数据库 | **SQLite** + **SQLAlchemy ORM** |
| 页面渲染 | **Jinja2** 服务端模板 |
| 前端 | HTML + CSS + **Chart.js** |
| AI | **DeepSeek API**（可选，无 Key 时使用 Mock 数据） |
| 测试 | **pytest** |
| 配置 | **python-dotenv**（.env 环境变量） |

> 利润计算会先按 `USD_CNY_RATE` 将人民币采购、头程和广告成本换算为美元，
> 再与美元售价、Amazon 佣金和 FBA 费用统一计算，避免混用币种。

---

## 📦 安装方法

### 1. 克隆项目

```bash
git clone <repo-url>
cd amazon-seller-ai-dashboard
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. （可选）配置 DeepSeek API Key

```bash
# 复制 .env.example 为 .env
cp .env.example .env

# 编辑 .env，填入你的 API Key
# 如果不填，项目会用 Mock 数据正常运行
# 可按实际情况调整 USD_CNY_RATE（默认 7.2）
```

---

## 🚀 启动方法

```bash
# 在项目根目录执行
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问：**http://127.0.0.1:8000**

会自动跳转到 Dashboard 页面。

---

## 🧪 运行测试

```bash
pytest tests/ -v
```

---

## 📸 项目截图

> 项目启动后，打开浏览器访问 http://127.0.0.1:8000 即可看到效果。
>
> 建议截图以下页面用于作品集展示：
> - Dashboard 首页（统计卡片 + 图表）
> - 商品管理列表页
> - 竞品分析列表页
> - 利润计算器（含计算结果）
> - AI 评论分析结果
> - AI Listing 优化结果

---

## 📁 项目结构

```
amazon-seller-ai-dashboard/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py           # 数据库连接配置
│   ├── models.py             # ORM 数据库模型
│   ├── schemas.py            # Pydantic 请求/响应模型
│   ├── crud.py               # 数据库增删改查操作
│   ├── routers/              # 路由（接口+页面）
│   │   ├── dashboard.py      #   首页 Dashboard
│   │   ├── products.py       #   商品管理
│   │   ├── competitors.py    #   竞品分析
│   │   ├── profit.py         #   利润计算器
│   │   └── ai.py             #   AI 评论分析 + Listing 优化
│   ├── services/             # 业务逻辑层
│   │   ├── profit_service.py #   利润计算核心逻辑
│   │   ├── ai_service.py     #   DeepSeek API 调用 / Mock
│   │   └── seed_service.py   #   种子数据
│   ├── templates/            # Jinja2 HTML 模板
│   └── static/css/           # 静态 CSS
├── tests/
│   └── test_profit_service.py # 利润计算单元测试
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LEARNING.md
```

---

## 🔮 后续规划

- [ ] 添加更多图表（销售趋势、利润变化）
- [ ] 支持 CSV 导入商品/竞品数据
- [ ] 添加日期范围筛选
- [ ] AI 评论情感分析可视化（正面/负面占比饼图）
- [ ] 添加定时任务（如库存预警邮件提醒）
- [ ] Docker 化部署
- [ ] 接入真实 DeepSeek / GPT API 对比测试
- [ ] 添加用户登录（简单版）

---

## 🎤 面试介绍话术

> "我独立开发了一个 **Amazon 跨境电商 AI 数据后台**，用于模拟卖家日常运营中的商品管理、竞品分析、利润测算、评论分析和 Listing 优化流程。
>
> 这个项目结合 **FastAPI + SQLAlchemy + Jinja2 + Chart.js** 全栈技术，并预留了 **DeepSeek API** 集成接口。我设计了完整的数据库模型（商品表、竞品表、利润表），封装了独立的利润计算引擎（含风险评级），并用 **pytest** 编写了单元测试。
>
> 通过这个项目，我不仅掌握了前后端协同开发的流程，也理解了 Amazon 跨境电商中选品、定价、利润模型和 Listing 优化的业务逻辑。"

---

## 📄 License

MIT — 仅供学习使用
