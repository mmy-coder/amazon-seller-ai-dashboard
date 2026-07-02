"""
Pydantic Schemas —— 用于 API 请求/响应的数据验证和序列化

为什么需要 schemas？
- models.py 定义的是数据库表结构
- schemas.py 定义的是 API 接口的输入/输出格式
- FastAPI 用 Pydantic 自动校验请求数据、生成 API 文档
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==================== Product Schemas ====================

class ProductBase(BaseModel):
    """商品的基础字段"""
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(default="")
    platform: str = Field(default="Amazon")
    purchase_cost: float = Field(default=0.0, ge=0)
    selling_price: float = Field(default=0.0, ge=0)
    inventory: int = Field(default=0, ge=0)
    status: str = Field(default="active")


class ProductCreate(ProductBase):
    """创建商品时的请求体"""
    pass


class ProductUpdate(BaseModel):
    """更新商品时的请求体（所有字段可选）"""
    name: Optional[str] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    purchase_cost: Optional[float] = None
    selling_price: Optional[float] = None
    inventory: Optional[int] = None
    status: Optional[str] = None


class ProductResponse(ProductBase):
    """返回给前端的商品数据"""
    id: int
    created_at: datetime
    competitor_count: int = 0  # 关联的竞品数量

    class Config:
        from_attributes = True  # 允许从 ORM 对象转换


# ==================== Competitor Schemas ====================

class CompetitorBase(BaseModel):
    """竞品的基础字段"""
    product_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=300)
    price: float = Field(default=0.0, ge=0)
    rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    url: str = Field(default="")
    main_selling_points: str = Field(default="")
    weakness: str = Field(default="")
    differentiation: str = Field(default="")


class CompetitorCreate(CompetitorBase):
    """创建竞品时的请求体"""
    pass


class CompetitorUpdate(BaseModel):
    """更新竞品时的请求体"""
    product_id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    url: Optional[str] = None
    main_selling_points: Optional[str] = None
    weakness: Optional[str] = None
    differentiation: Optional[str] = None


class CompetitorResponse(CompetitorBase):
    """返回给前端的竞品数据"""
    id: int
    created_at: datetime
    product_name: str = ""  # 关联商品的名称

    class Config:
        from_attributes = True


# ==================== Profit Schemas ====================

class ProfitCalculateRequest(BaseModel):
    """利润计算请求"""
    product_name: str = Field(..., min_length=1, max_length=200)
    purchase_cost: float = Field(..., ge=0, description="采购成本（人民币）")
    selling_price: float = Field(..., gt=0, description="售价（美元）")
    shipping_cost: float = Field(default=0.0, ge=0, description="头程/物流成本")
    amazon_fee_rate: float = Field(default=0.15, ge=0, le=1, description="Amazon 佣金比例")
    fba_fee: float = Field(default=0.0, ge=0, description="FBA 履约费用")
    ad_cost: float = Field(default=0.0, ge=0, description="广告成本")
    return_rate: float = Field(default=0.03, ge=0, le=1, description="退货率")


class ProfitCalculateResponse(BaseModel):
    """利润计算结果"""
    product_name: str
    purchase_cost: float
    selling_price: float
    shipping_cost: float
    amazon_fee_rate: float
    fba_fee: float
    ad_cost: float
    return_rate: float
    gross_revenue: float
    total_cost: float
    estimated_profit: float
    profit_margin: float
    break_even_price: float
    risk_level: str

    class Config:
        from_attributes = True


class ProfitRecordResponse(ProfitCalculateResponse):
    """利润记录（含数据库 ID 和时间）"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== AI Schemas ====================

class ReviewAnalysisRequest(BaseModel):
    """AI 评论分析请求"""
    reviews: str = Field(..., min_length=10, description="用户粘贴的评论文本")


class ReviewAnalysisResponse(BaseModel):
    """AI 评论分析结果"""
    pain_points: str = ""        # 用户主要痛点
    positive_points: str = ""    # 高频好评点
    negative_points: str = ""    # 高频差评点
    improvement_suggestions: str = ""  # 产品改进建议
    listing_suggestions: str = ""      # Listing 优化建议
    selling_points: str = ""     # 可提炼的卖点


class ListingOptimizeRequest(BaseModel):
    """AI Listing 优化请求"""
    product_name: str = Field(..., min_length=1)
    category: str = Field(default="")
    core_selling_points: str = Field(default="")
    target_users: str = Field(default="")
    competitor_weakness: str = Field(default="")
    user_pain_points: str = Field(default="")


class ListingOptimizeResponse(BaseModel):
    """AI Listing 优化结果"""
    title_suggestions: str = ""      # 标题建议
    bullet_points: str = ""          # 五点描述
    search_keywords: str = ""        # 搜索关键词
    product_description: str = ""    # 产品描述
    differentiation_points: str = "" # 差异化卖点


# ==================== Dashboard Schemas ====================

class DashboardStats(BaseModel):
    """Dashboard 统计数据"""
    total_products: int = 0
    total_competitors: int = 0
    avg_profit_margin: float = 0.0
    low_inventory_count: int = 0     # 库存预警（库存<10）
    high_risk_count: int = 0         # 高风险利润测算数
