"""
CRUD 操作层 —— 封装所有数据库增删改查

CRUD = Create（创建）、Read（读取）、Update（更新）、Delete（删除）

为什么要有这一层？
- 将数据库操作与路由逻辑分离
- routers 调用 crud，crud 操作数据库
- 便于复用和测试
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


# ==================== Product CRUD ====================


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """获取商品列表"""
    products = (
        db.query(models.Product)
        .order_by(models.Product.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    # 给每个 product 附加竞品数量
    for p in products:
        p.competitor_count = len(p.competitors)
    return products


def get_product(db: Session, product_id: int):
    """获取单个商品"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.competitor_count = len(product.competitors)
    return product


def create_product(db: Session, product_data: dict):
    """创建商品"""
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product_data: dict):
    """更新商品（只更新传入的字段）"""
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if not db_product:
        return None
    for key, value in product_data.items():
        if value is not None:
            setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    """删除商品"""
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


# ==================== Competitor CRUD ====================


def get_competitors(db: Session, skip: int = 0, limit: int = 100):
    """获取竞品列表（含关联商品名）"""
    competitors = (
        db.query(models.Competitor)
        .order_by(models.Competitor.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    for c in competitors:
        c.product_name = c.product.name if c.product else ""
    return competitors


def get_competitor(db: Session, competitor_id: int):
    """获取单个竞品"""
    competitor = (
        db.query(models.Competitor)
        .filter(models.Competitor.id == competitor_id)
        .first()
    )
    if competitor:
        competitor.product_name = competitor.product.name if competitor.product else ""
    return competitor


def get_competitors_by_product(db: Session, product_id: int):
    """获取某商品的所有竞品"""
    return (
        db.query(models.Competitor)
        .filter(models.Competitor.product_id == product_id)
        .all()
    )


def create_competitor(db: Session, competitor_data: dict):
    """创建竞品"""
    db_competitor = models.Competitor(**competitor_data)
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    db_competitor.product_name = (
        db_competitor.product.name if db_competitor.product else ""
    )
    return db_competitor


def update_competitor(db: Session, competitor_id: int, competitor_data: dict):
    """更新竞品"""
    db_competitor = (
        db.query(models.Competitor)
        .filter(models.Competitor.id == competitor_id)
        .first()
    )
    if not db_competitor:
        return None
    for key, value in competitor_data.items():
        if value is not None:
            setattr(db_competitor, key, value)
    db.commit()
    db.refresh(db_competitor)
    db_competitor.product_name = (
        db_competitor.product.name if db_competitor.product else ""
    )
    return db_competitor


def delete_competitor(db: Session, competitor_id: int):
    """删除竞品"""
    db_competitor = (
        db.query(models.Competitor)
        .filter(models.Competitor.id == competitor_id)
        .first()
    )
    if not db_competitor:
        return False
    db.delete(db_competitor)
    db.commit()
    return True


# ==================== Profit CRUD ====================


def create_profit_record(db: Session, profit_data: dict):
    """保存利润测算记录"""
    db_record = models.ProfitRecord(**profit_data)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_profit_records(db: Session, skip: int = 0, limit: int = 50):
    """获取利润测算历史"""
    return (
        db.query(models.ProfitRecord)
        .order_by(models.ProfitRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_profit_record(db: Session, record_id: int):
    """获取单条利润记录"""
    return (
        db.query(models.ProfitRecord)
        .filter(models.ProfitRecord.id == record_id)
        .first()
    )


def delete_profit_record(db: Session, record_id: int):
    """删除利润记录"""
    db_record = (
        db.query(models.ProfitRecord)
        .filter(models.ProfitRecord.id == record_id)
        .first()
    )
    if not db_record:
        return False
    db.delete(db_record)
    db.commit()
    return True


# ==================== Dashboard 统计 ====================


def get_dashboard_stats(db: Session):
    """获取 Dashboard 统计数据"""
    total_products = db.query(func.count(models.Product.id)).scalar() or 0
    total_competitors = db.query(func.count(models.Competitor.id)).scalar() or 0

    avg_margin = db.query(func.avg(models.ProfitRecord.profit_margin)).scalar() or 0.0

    # 库存预警：库存小于 10 的商品
    low_inventory = (
        db.query(func.count(models.Product.id))
        .filter(models.Product.inventory < 10, models.Product.status == "active")
        .scalar()
        or 0
    )

    # 高风险利润测算
    high_risk = (
        db.query(func.count(models.ProfitRecord.id))
        .filter(models.ProfitRecord.risk_level == "high")
        .scalar()
        or 0
    )

    return {
        "total_products": total_products,
        "total_competitors": total_competitors,
        "avg_profit_margin": round(avg_margin, 1),
        "low_inventory_count": low_inventory,
        "high_risk_count": high_risk,
    }


def get_recent_products(db: Session, limit: int = 5):
    """获取最近添加的商品"""
    return (
        db.query(models.Product)
        .order_by(models.Product.created_at.desc())
        .limit(limit)
        .all()
    )


def get_product_status_distribution(db: Session):
    """商品状态分布"""
    results = (
        db.query(models.Product.status, func.count(models.Product.id))
        .group_by(models.Product.status)
        .all()
    )
    return [{"status": r[0], "count": r[1]} for r in results]


def get_product_category_distribution(db: Session):
    """商品类目分布"""
    results = (
        db.query(models.Product.category, func.count(models.Product.id))
        .group_by(models.Product.category)
        .all()
    )
    return [{"category": r[0] or "未分类", "count": r[1]} for r in results]


def get_recent_profit_records(db: Session, limit: int = 5):
    """获取最近的利润测算"""
    return (
        db.query(models.ProfitRecord)
        .order_by(models.ProfitRecord.created_at.desc())
        .limit(limit)
        .all()
    )
