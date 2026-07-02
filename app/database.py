"""
数据库配置和会话管理

用 SQLAlchemy 连接 SQLite，创建 engine、SessionLocal 和 Base。
SQLite 适合学习和小型项目，不需要额外安装数据库服务。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite 数据库文件路径（项目根目录下的 amazon_dashboard.db）
SQLALCHEMY_DATABASE_URL = "sqlite:///amazon_dashboard.db"

# engine 是 SQLAlchemy 与数据库的连接核心
# connect_args={"check_same_thread": False} 是因为 FastAPI 是多线程的，SQLite 默认不允许跨线程
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 多线程兼容
    echo=False,  # 设置为 True 可以查看 SQL 日志
)

# SessionLocal 是每个请求使用的数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 是所有 ORM 模型的基类
Base = declarative_base()


def get_db():
    """
    FastAPI 依赖注入：每个请求获取一个数据库会话，请求结束后自动关闭。

    用法：
        @router.get("/")
        def some_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
