"""
数据库模型定义

每个 class 对应数据库中的一张表。
字段 = 列定义（列名、类型、约束）。
关系 = 表与表之间的关联（如 Product 与 Competitor 的一对多关系）。
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Product(Base):
    """
    商品表 —— 模拟卖家管理自己的产品池

    业务含义：
    - 每个商品有采购成本（purchase_cost）和售价（selling_price）
    - 库存（inventory）用于库存预警
    - 状态（status）标记商品运营阶段：active（在售）/ testing（测试中）/ stopped（已停售）
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="商品名")
    category = Column(String(100), default="", comment="类目")
    platform = Column(String(50), default="Amazon", comment="平台")
    purchase_cost = Column(Float, default=0.0, comment="采购成本（人民币）")
    selling_price = Column(Float, default=0.0, comment="售价（美元）")
    inventory = Column(Integer, default=0, comment="库存数量")
    status = Column(String(20), default="active", comment="状态：active/testing/stopped")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")

    # 一个商品可以有多个竞品分析记录
    competitors = relationship("Competitor", back_populates="product", cascade="all, delete-orphan")


class Competitor(Base):
    """
    竞品表 —— 用于竞品调研和选品分析

    业务含义：
    - 每个竞品关联一个我方商品（product_id）
    - 记录竞品的价格、评分、评论数等关键指标
    - main_selling_points（主要卖点）：竞品做对了什么
    - weakness（竞品弱点）：竞品的不足之处
    - differentiation（差异化机会）：基于弱点，我方能做什么不同的事
    """
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="关联商品ID")
    title = Column(String(300), nullable=False, comment="竞品标题")
    price = Column(Float, default=0.0, comment="竞品价格（美元）")
    rating = Column(Float, default=0.0, comment="评分（1-5）")
    review_count = Column(Integer, default=0, comment="评论数")
    url = Column(String(500), default="", comment="竞品链接")
    main_selling_points = Column(Text, default="", comment="主要卖点")
    weakness = Column(Text, default="", comment="竞品弱点")
    differentiation = Column(Text, default="", comment="我方差异化机会")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")

    product = relationship("Product", back_populates="competitors")


class ProfitRecord(Base):
    """
    利润测算记录表 —— 记录每次利润测算

    业务含义：
    - 模拟 Amazon 卖家在选品阶段的利润测算
    - 输入各项成本（采购、物流、佣金、FBA、广告、退货）
    - 计算出利润、利润率、保本售价、风险等级
    - 帮助判断一个产品值不值得做

    关键公式：
    - gross_revenue = selling_price（简化：一件的销售收入）
    - total_cost = purchase_cost + shipping_cost + amazon_fee + fba_fee + ad_cost + return_loss
    - estimated_profit = gross_revenue - total_cost
    - profit_margin = estimated_profit / gross_revenue * 100%
    - break_even_price = total_cost（卖这个价刚好不亏不赚）
    """
    __tablename__ = "profit_records"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False, comment="商品名")
    purchase_cost = Column(Float, default=0.0, comment="采购成本")
    selling_price = Column(Float, default=0.0, comment="售价")
    shipping_cost = Column(Float, default=0.0, comment="头程/物流成本")
    amazon_fee_rate = Column(Float, default=0.15, comment="Amazon 佣金比例（默认15%）")
    fba_fee = Column(Float, default=0.0, comment="FBA 或履约费用")
    ad_cost = Column(Float, default=0.0, comment="广告成本")
    return_rate = Column(Float, default=0.03, comment="退货率（默认3%）")

    # 计算结果
    gross_revenue = Column(Float, default=0.0, comment="销售收入")
    total_cost = Column(Float, default=0.0, comment="总成本")
    estimated_profit = Column(Float, default=0.0, comment="预估利润")
    profit_margin = Column(Float, default=0.0, comment="利润率（%）")
    break_even_price = Column(Float, default=0.0, comment="保本售价")
    risk_level = Column(String(20), default="medium", comment="风险等级：low/medium/high")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间")
