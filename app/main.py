"""
FastAPI 应用入口 —— Amazon Seller AI Dashboard

这个文件负责：
1. 创建 FastAPI 应用实例
2. 配置 Jinja2 模板引擎
3. 注册所有路由
4. 启动时创建数据库表 + 插入种子数据
5. 将首页重定向到 Dashboard
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from app.database import engine, Base, SessionLocal
from app.services.seed_service import seed_data_if_empty

# 导入所有路由
from app.routers import dashboard, products, competitors, profit, ai


# ===== 创建 FastAPI 应用 =====
app = FastAPI(
    title="Amazon Seller AI Dashboard",
    description="Amazon 跨境电商 AI 数据后台 - 学习/演示版",
    version="1.0.0",
)

# ===== 配置 Jinja2 模板引擎 =====
# Jinja2 是 Python 最流行的模板引擎，可以把数据渲染成 HTML 页面。
# 类似于：HTML 模板 + 数据 = 最终页面

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)


class Jinja2Templates:
    """简易 Jinja2 模板包装器，方便在路由中使用"""

    def __init__(self, env: Environment):
        self.env = env

    def TemplateResponse(self, name: str, context: dict):
        """模拟 Starlette 的 TemplateResponse，返回 HTML"""
        from starlette.responses import HTMLResponse

        template = self.env.get_template(name)
        content = template.render(**context)
        return HTMLResponse(content=content)


# 将模板引擎挂载到 app.state，路由里通过 request.app.state.templates 访问
app.state.templates = Jinja2Templates(jinja_env)

# ===== 挂载静态文件（CSS、JS 等） =====
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ===== 注册路由 =====
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(competitors.router)
app.include_router(profit.router)
app.include_router(ai.router)


# ===== 首页重定向 =====
@app.get("/")
async def root():
    """访问根路径时自动跳转到 Dashboard"""
    return RedirectResponse(url="/dashboard")


# ===== 启动事件 =====
@app.on_event("startup")
def startup():
    """应用启动时：创建数据库表、插入种子数据"""
    # 创建所有表（如果表不存在会自动创建）
    Base.metadata.create_all(bind=engine)

    # 插入种子数据（仅在数据为空时）
    db = SessionLocal()
    try:
        seed_data_if_empty(db)
    finally:
        db.close()

    print("Amazon Seller AI Dashboard started successfully!")
    print("Visit: http://127.0.0.1:8000/dashboard")
