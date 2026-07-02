"""
种子数据服务 —— 启动时自动插入演示数据

设计思路：
- 检查数据库是否已有数据
- 如果为空，插入预设的演示数据
- 不会重复插入

包含：
- 3个商品（Wireless Neck Fan, Portable Blender, Laptop Stand）
- 每个商品 2 个竞品（共 6 个竞品）
- 3 条利润测算记录
"""

from sqlalchemy.orm import Session
from app import models
from app.services.profit_service import calculate_profit


def seed_data_if_empty(db: Session):
    """
    如果数据库为空，插入种子数据。

    用法：在 FastAPI 启动事件中调用
        @app.on_event("startup")
        def startup():
            seed_data_if_empty(next(get_db()))
    """

    # 检查是否已有数据
    existing_products = db.query(models.Product).count()
    if existing_products > 0:
        print("DB already has data, skip seeding")
        return

    print("DB is empty, inserting seed data...")

    # ===== 商品1：Wireless Neck Fan =====
    p1 = models.Product(
        name="Wireless Neck Fan",
        category="Personal Cooling",
        platform="Amazon",
        purchase_cost=35.0,
        selling_price=25.99,
        inventory=120,
        status="active",
    )
    db.add(p1)
    db.flush()  # 获取 p1.id

    c1_1 = models.Competitor(
        product_id=p1.id,
        title="Portable Neck Fan, 4000mAh Rechargeable Personal Fan, Hands Free Bladeless Fan",
        price=22.99,
        rating=4.2,
        review_count=1523,
        url="https://www.amazon.com/dp/B0EXAMPLE1",
        main_selling_points="价格较低，4000mAh电池，无叶设计",
        weakness="续航实际只有3小时，噪音偏大（45dB+），材质廉价",
        differentiation="升级4800mAh电池（6h续航），降噪技术（<40dB），亲肤材质",
    )
    c1_2 = models.Competitor(
        product_id=p1.id,
        title="Bladeless Neck Fan, 360° Cooling, 3 Speed, USB Rechargeable, Lightweight",
        price=29.99,
        rating=4.4,
        review_count=2301,
        url="https://www.amazon.com/dp/B0EXAMPLE2",
        main_selling_points="360°环绕出风，设计感强，品牌知名度高",
        weakness="价格偏高，重量190g偏重，颜色选择少（仅黑白）",
        differentiation="更轻量化（180g以下），多配色选择，性价比更高",
    )
    db.add_all([c1_1, c1_2])

    # ===== 商品2：Portable Blender =====
    p2 = models.Product(
        name="Portable Blender",
        category="Kitchen & Dining",
        platform="Amazon",
        purchase_cost=45.0,
        selling_price=35.99,
        inventory=80,
        status="active",
    )
    db.add(p2)
    db.flush()

    c2_1 = models.Competitor(
        product_id=p2.id,
        title="Portable Blender, 20oz Personal Blender for Shakes and Smoothies, USB Rechargeable",
        price=32.99,
        rating=4.0,
        review_count=892,
        url="https://www.amazon.com/dp/B0EXAMPLE3",
        main_selling_points="价格低，20oz容量，USB充电方便",
        weakness="电机力量不足（搅不动冰块），密封圈易坏，清洗不便",
        differentiation="升级强力电机（可碎冰），食品级硅胶密封圈，一键清洗功能",
    )
    c2_2 = models.Competitor(
        product_id=p2.id,
        title="Mini Blender, 380ml, 6 Blades, Portable Juicer, Magnetic Charging",
        price=39.99,
        rating=4.5,
        review_count=3200,
        url="https://www.amazon.com/dp/B0EXAMPLE4",
        main_selling_points="6叶刀片搅打细腻，磁吸充电，品牌销量第一",
        weakness="价格最高，380ml容量偏小，磁吸充电线不兼容其他设备",
        differentiation="大容量（450ml），Type-C通用充电，性价比更高",
    )
    db.add_all([c2_1, c2_2])

    # ===== 商品3：Laptop Stand =====
    p3 = models.Product(
        name="Laptop Stand",
        category="Office Products",
        platform="Amazon",
        purchase_cost=25.0,
        selling_price=19.99,
        inventory=200,
        status="active",
    )
    db.add(p3)
    db.flush()

    c3_1 = models.Competitor(
        product_id=p3.id,
        title="Adjustable Laptop Stand, Aluminum, Ergonomic, Foldable, Compatible with 10-17 inch Laptops",
        price=18.99,
        rating=4.3,
        review_count=4500,
        url="https://www.amazon.com/dp/B0EXAMPLE5",
        main_selling_points="铝合金材质，可折叠便携，价格低，兼容性好",
        weakness="高度调节档位少（仅3档），稳定性一般，防滑垫容易脱落",
        differentiation="6档高度可调，加强防滑硅胶垫，附赠收纳袋",
    )
    c3_2 = models.Competitor(
        product_id=p3.id,
        title="Premium Laptop Riser, Ventilated, Cable Management, Multi-Device Stand",
        price=24.99,
        rating=4.6,
        review_count=1800,
        url="https://www.amazon.com/dp/B0EXAMPLE6",
        main_selling_points="散热设计好，线缆管理，支持多设备，高级感强",
        weakness="价格最高，不可折叠（占空间），重量1.5kg不便携",
        differentiation="轻量化折叠设计，同样的散热性能，价格更低",
    )
    db.add_all([c3_1, c3_2])

    # ===== 3条利润测算记录 =====
    profit_data_1 = calculate_profit(
        purchase_cost=35.0,
        selling_price=25.99,
        shipping_cost=8.0,
        amazon_fee_rate=0.15,
        fba_fee=3.5,
        ad_cost=2.0,
        return_rate=0.03,
    )
    pr1 = models.ProfitRecord(
        product_name="Wireless Neck Fan",
        purchase_cost=35.0,
        selling_price=25.99,
        shipping_cost=8.0,
        amazon_fee_rate=0.15,
        fba_fee=3.5,
        ad_cost=2.0,
        return_rate=0.03,
        gross_revenue=profit_data_1["gross_revenue"],
        total_cost=profit_data_1["total_cost"],
        estimated_profit=profit_data_1["estimated_profit"],
        profit_margin=profit_data_1["profit_margin"],
        break_even_price=profit_data_1["break_even_price"],
        risk_level=profit_data_1["risk_level"],
    )
    db.add(pr1)

    profit_data_2 = calculate_profit(
        purchase_cost=45.0,
        selling_price=35.99,
        shipping_cost=10.0,
        amazon_fee_rate=0.15,
        fba_fee=4.0,
        ad_cost=3.0,
        return_rate=0.04,
    )
    pr2 = models.ProfitRecord(
        product_name="Portable Blender",
        purchase_cost=45.0,
        selling_price=35.99,
        shipping_cost=10.0,
        amazon_fee_rate=0.15,
        fba_fee=4.0,
        ad_cost=3.0,
        return_rate=0.04,
        gross_revenue=profit_data_2["gross_revenue"],
        total_cost=profit_data_2["total_cost"],
        estimated_profit=profit_data_2["estimated_profit"],
        profit_margin=profit_data_2["profit_margin"],
        break_even_price=profit_data_2["break_even_price"],
        risk_level=profit_data_2["risk_level"],
    )
    db.add(pr2)

    profit_data_3 = calculate_profit(
        purchase_cost=25.0,
        selling_price=19.99,
        shipping_cost=5.0,
        amazon_fee_rate=0.15,
        fba_fee=2.5,
        ad_cost=1.5,
        return_rate=0.02,
    )
    pr3 = models.ProfitRecord(
        product_name="Laptop Stand",
        purchase_cost=25.0,
        selling_price=19.99,
        shipping_cost=5.0,
        amazon_fee_rate=0.15,
        fba_fee=2.5,
        ad_cost=1.5,
        return_rate=0.02,
        gross_revenue=profit_data_3["gross_revenue"],
        total_cost=profit_data_3["total_cost"],
        estimated_profit=profit_data_3["estimated_profit"],
        profit_margin=profit_data_3["profit_margin"],
        break_even_price=profit_data_3["break_even_price"],
        risk_level=profit_data_3["risk_level"],
    )
    db.add(pr3)

    db.commit()
    print(f"Seed data inserted: {3} products, {6} competitors, {3} profit records")
