"""
利润计算服务

这是本项目的核心业务逻辑之一，模拟 Amazon 卖家在选品阶段的利润测算。

真实 Amazon 运营中，卖家需要计算：
1. 采购成本：从供应商拿货的成本（人民币）
2. 头程物流：海运/空运到 Amazon 仓库的费用
3. Amazon 佣金：平台按售价百分比收取的佣金（通常 15%）
4. FBA 费用：Fulfillment by Amazon，物流配送费
5. 广告费用：PPC（按点击付费）广告成本
6. 退货损失：退货产生的平均损失

通过这些数据，可以算出：
- 每卖一件能赚多少钱（estimated_profit）
- 利润率是多少（profit_margin）
- 卖多少钱才不亏（break_even_price）
- 风险有多大（risk_level）
"""


def calculate_profit(
    purchase_cost: float,
    selling_price: float,
    shipping_cost: float = 0.0,
    amazon_fee_rate: float = 0.15,
    fba_fee: float = 0.0,
    ad_cost: float = 0.0,
    return_rate: float = 0.03,
    exchange_rate: float = 7.2,
) -> dict:
    """
    利润计算核心函数

    Args:
        purchase_cost: 采购成本（人民币）
        selling_price: 售价（美元）
        shipping_cost: 头程/物流成本（人民币）
        amazon_fee_rate: Amazon 佣金比例，默认 15%（0.15）
        fba_fee: FBA 履约费用
        ad_cost: 广告成本（人民币）
        return_rate: 退货率，默认 3%（0.03）
        exchange_rate: 1 美元可兑换的人民币金额，例如 7.2

    Returns:
        dict: 包含所有计算结果
    """

    if exchange_rate <= 0:
        raise ValueError("汇率必须大于 0")

    # 人民币成本先换算成美元，避免不同币种直接相减。
    purchase_cost_usd = purchase_cost / exchange_rate
    shipping_cost_usd = shipping_cost / exchange_rate
    ad_cost_usd = ad_cost / exchange_rate

    # 计算销售收入（简化：一件的售价就是一件商品的收入）
    # 真实场景中 gross_revenue 就是 selling_price（一件商品的销售收入）
    gross_revenue = selling_price

    # 计算各项成本
    amazon_fee = selling_price * amazon_fee_rate  # Amazon 平台佣金
    return_loss = selling_price * return_rate      # 退货损失（按售价比例估算）

    # 总成本 = 采购 + 物流 + Amazon佣金 + FBA + 广告 + 退货损失
    total_cost = (
        purchase_cost_usd
        + shipping_cost_usd
        + amazon_fee
        + fba_fee
        + ad_cost_usd
        + return_loss
    )

    # 预估利润 = 收入 - 总成本
    estimated_profit = gross_revenue - total_cost

    # 利润率 = (利润 / 销售收入) * 100
    if gross_revenue > 0:
        profit_margin = round((estimated_profit / gross_revenue) * 100, 2)
    else:
        profit_margin = 0.0

    # 保本售价 —— 需要把百分比成本（佣金+退货）也算进去
    # 公式推导：
    #   break_even_price = purchase_cost + shipping_cost + fba_fee + ad_cost
    #                       + break_even_price * amazon_fee_rate
    #                       + break_even_price * return_rate
    #   移项 → break_even_price * (1 - amazon_fee_rate - return_rate) = 固定成本
    #   所以 → break_even_price = 固定成本 / (1 - amazon_fee_rate - return_rate)
    percentage_rate = amazon_fee_rate + return_rate
    if percentage_rate < 1:
        fixed_costs = purchase_cost_usd + shipping_cost_usd + fba_fee + ad_cost_usd
        break_even_price = round(fixed_costs / (1 - percentage_rate), 2)
    else:
        # 极端情况：费率 >= 100%，无法保本
        break_even_price = float("inf")

    # 风险等级判定
    # - 利润率 >= 25%：低风险（利润空间充足）
    # - 10% <= 利润率 < 25%：中等风险（可以尝试，需精细运营）
    # - 利润率 < 10%：高风险（很容易亏损）
    if profit_margin >= 25:
        risk_level = "low"
    elif profit_margin >= 10:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "exchange_rate": round(exchange_rate, 4),
        "purchase_cost_usd": round(purchase_cost_usd, 2),
        "shipping_cost_usd": round(shipping_cost_usd, 2),
        "ad_cost_usd": round(ad_cost_usd, 2),
        "gross_revenue": round(gross_revenue, 2),
        "total_cost": round(total_cost, 2),
        "estimated_profit": round(estimated_profit, 2),
        "profit_margin": profit_margin,
        "break_even_price": break_even_price,
        "risk_level": risk_level,
    }
