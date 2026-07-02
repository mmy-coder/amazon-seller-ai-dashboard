# 学习指南 —— 从 0 理解这个项目

> 如果你是第一次接触 Web 全栈开发，别着急，跟着这个文档一步一步来。

---

## 一、整体架构

这个项目使用了经典的 **"三层架构"**：

```
浏览器 → Router（路由） → Service（业务逻辑） → CRUD（数据库操作） → SQLite
         ↑                ↑                    ↑
      Jinja2 模板      利润计算/AI调用        SQLAlchemy ORM
```

简单来说就是：
1. 用户在浏览器点一个链接/提交一个表单
2. FastAPI **Router** 接收请求
3. Router 调用 **Service** 层的业务逻辑
4. Service 需要存数据时调用 **CRUD** 层
5. CRUD 用 SQLAlchemy 操作 **SQLite 数据库**
6. 结果通过 **Jinja2 模板** 渲染成 HTML 返回给浏览器

---

## 二、每个目录/文件的作用

### `app/main.py` —— 启动入口
FastAPI 从这里启动。
- 创建 FastAPI 应用
- 配置 Jinja2 模板引擎
- 注册所有路由
- 启动时自动创建数据库表、插入种子数据

### `app/database.py` —— 数据库连接
配置 SQLAlchemy 连接 SQLite。`get_db()` 函数是 FastAPI 的依赖注入，每个请求自动获取和释放数据库会话。

### `app/models.py` —— 数据库模型
定义数据库表结构。每个 class 对应一张表，每个属性对应一个字段。
SQLAlchemy 会自动把这些 class 转成数据库表。

### `app/schemas.py` —— 请求/响应模型
Pydantic 数据验证。定义 API 接口需要什么输入、返回什么输出。FastAPI 用这个自动生成 API 文档。

### `app/crud.py` —— 数据库操作
封装所有"增删改查"操作。Routers 只调用 CRUD 函数，不直接写 SQL。

### `app/routers/` —— 路由（接口+页面）
每个文件处理一类功能：
- `dashboard.py`：首页数据看板
- `products.py`：商品 CRUD
- `competitors.py`：竞品 CRUD
- `profit.py`：利润计算
- `ai.py`：AI 功能

### `app/services/` —— 业务逻辑
- `profit_service.py`：利润计算核心（纯数学逻辑，不依赖数据库）
- `ai_service.py`：调用 DeepSeek API 或返回 Mock 数据
- `seed_service.py`：插入演示数据

### `app/templates/` —— HTML 模板
Jinja2 模板文件。`base.html` 是基础布局，其他页面继承它。
Jinja2 语法：`{{ 变量 }}` 输出数据，`{% if/for %}` 是控制流。

### `app/static/css/` —— 样式
纯手写 CSS，没有用框架。方便学习理解。

---

## 三、关键概念解释

### FastAPI 是怎么启动的？

```
uvicorn app.main:app --reload
       │          │     │
       │          │     └── 热重载（代码变动自动重启）
       │          └── FastAPI 应用实例
       └── ASGI 服务器
```

`uvicorn` 是一个 ASGI 服务器，它运行 FastAPI 应用并监听 HTTP 请求。

### Router 是什么？

Router = 路由器。它把 HTTP 请求（如 `GET /products`）分发到对应的处理函数。

```python
@router.get("/")      # 访问 /products 时
async def product_list():  # 执行这个函数
    ...
```

装饰器 `@router.get("/products/{id}/edit")` 中的 `{id}` 是路径参数，会自动传给函数。

### Model 是什么？

Model = 数据模型 = 数据库表的 Python 表示。

```python
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
```

这段代码告诉 SQLAlchemy：数据库里有一张叫 `products` 的表，有 `id` 和 `name` 两个字段。当你在 Python 里操作 `Product` 对象时，SQLAlchemy 自动把它翻译成 SQL 语句执行。

### CRUD 是什么？

CRUD = Create（创建）、Read（读取）、Update（更新）、Delete（删除）。是数据库最基本的 4 种操作。

### Service 层是什么？

业务逻辑层。把"怎么做一件事"的逻辑从路由中抽出来。

- 路由只负责：接收请求 → 调用 service → 返回结果
- Service 负责：实际的计算逻辑或外部 API 调用

这样写的好处：同样的利润计算逻辑，可以在网页里用，也可以在测试里用，不用重复写。

### Jinja2 模板如何返回页面？

```python
return request.app.state.templates.TemplateResponse(
    "products.html",
    {"request": request, "products": products}
)
```

Jinja2 读取 `products.html` 模板，把 `products` 这个 Python 列表填进去，渲染成完整的 HTML 页面，返回给浏览器。

### SQLite 数据如何保存？

1. 你通过网页提交表单（如新增商品）
2. Router 拿到表单数据，调用 CRUD 的 `create_product()`
3. CRUD 创建 `Product` 对象，调用 `db.add()` 和 `db.commit()`
4. SQLAlchemy 生成 `INSERT INTO products ...` SQL 语句
5. SQLite 执行 SQL，把数据写入 `amazon_dashboard.db` 文件

**SQLite 的好处**：不需要安装任何数据库软件，所有数据存到一个文件里，拷走就行。

---

## 四、业务逻辑学习

### 利润计算如何对应真实 Amazon 运营？

真实运营中，每卖一件产品的利润是这样算的：

```
利润 = 售价 - (采购成本 + 物流费 + Amazon佣金 + FBA费 + 广告费 + 退货损失)
```

- **Amazon 佣金**：平台抽成，一般是售价的 15%
- **FBA 费**：Fulfillment by Amazon，Amazon 帮你打包发货的费用
- **广告费**：PPC（按点击付费）广告，摊到每件产品上
- **退货损失**：退货产生的运费和产品损耗

这个项目模拟了这个完整流程，帮你理解选品时如何评估产品的盈利空间。

### 竞品分析如何对应选品？

真实选品中，卖家需要：
1. 找到目标市场的竞品
2. 分析竞品的卖点（他们在强调什么）
3. 分析竞品的弱点（用户在抱怨什么）
4. 找到差异化的机会（我能做什么不同的）

这个项目的竞品表就是为了支撑这套分析逻辑。

### AI 评论分析如何帮助改品？

Amazon 评论是"金矿"——用户直接告诉你他们喜欢什么、讨厌什么。

AI 评论分析帮你：
- 快速提取高频痛点 → 决定改进方向
- 识别好评点 → 知道哪些卖点最有吸引力
- 提炼卖点 → 用于写 Listing 和五点描述

### Listing 优化如何帮助转化？

Listing = Amazon 产品详情页。好的 Listing 带来更多点击和转化。

AI 优化帮你：
- 写含关键词的标题 → 提高搜索排名
- 写吸引人的五点描述 → 提高转化率
- 提炼差异化卖点 → 在竞争中脱颖而出

---

## 五、学习路线建议

### 第一步：看这些文件（按顺序）

1. **`app/main.py`** —— 了解应用如何启动
2. **`app/database.py`** —— 了解数据库怎么连
3. **`app/models.py`** —— 看看有哪些表、哪些字段
4. **`app/services/profit_service.py`** —— 核心业务逻辑，最简单
5. **`app/routers/dashboard.py`** —— 看看首页怎么渲染
6. **`app/routers/products.py`** —— 看看 CRUD 怎么实现
7. **`app/crud.py`** —— 数据库操作细节
8. **`app/services/ai_service.py`** —— AI 调用逻辑
9. **`app/templates/base.html`** —— 页面布局基础
10. **`tests/test_profit_service.py`** —— 测试怎么写

### 第二步：运行时加 print

在代码里加 `print()` 看看数据是怎么流转的。例如在 `app/routers/products.py` 的 `product_create` 函数里加个 `print(name, category)`。

### 第三步：尝试改代码

比如改改 CSS 颜色、加个字段、改改利润计算的风险阈值。

---

## 六、下一步可以自己改的功能

以下是推荐你自己动手修改的 5 个功能，从简单到复杂：

1. **改 CSS 主题色** → 把 `:root` 里的 `--primary` 改个颜色，看整体风格变化
2. **给商品表加字段** → 比如加个 `supplier`（供应商）字段，体会从 model → schema → form → 页面 的完整链路
3. **改风险等级阈值** → 把 25%/10% 改成其他值，看利润计算结果的变化
4. **加一个导出功能** → 在利润页面加个"导出 CSV"按钮，学习文件下载
5. **接真实 DeepSeek API** → 申请免费的 DeepSeek API Key，配到 .env 里，体验真正的 AI 返回效果

---

祝你学习愉快！🚀
