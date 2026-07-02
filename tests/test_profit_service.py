"""
利润计算服务测试

测试目标：验证 profit_service.calculate_profit 的计算逻辑是否正确。

测试覆盖：
- 正常盈利场景
- 亏损场景
- 高利润率（低风险）
- 中等利润率（中风险）
- 低利润率（高风险）
- 零售价边界情况
- 退货率影响
- 保本售价正确性
"""

import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.profit_service import calculate_profit


class TestProfitCalculation:
    """测试利润计算核心逻辑"""

    def test_normal_profit_scenario(self):
        """正常盈利场景：Wireless Neck Fan 模拟"""
        result = calculate_profit(
            purchase_cost=35.0,
            selling_price=25.99,
            shipping_cost=8.0,
            amazon_fee_rate=0.15,
            fba_fee=3.5,
            ad_cost=2.0,
            return_rate=0.03,
        )

        # 手动验算
        # gross_revenue = 25.99
        # amazon_fee = 25.99 * 0.15 = 3.8985
        # return_loss = 25.99 * 0.03 = 0.7797
        # total_cost = 35 + 8 + 3.8985 + 3.5 + 2 + 0.7797 = 53.1782
        # estimated_profit = 25.99 - 53.1782 = -27.1882 (亏损！)

        assert result["gross_revenue"] == 25.99
        assert result["total_cost"] == round(35 + 8 + 25.99 * 0.15 + 3.5 + 2 + 25.99 * 0.03, 2)
        assert result["estimated_profit"] < 0  # 这个案例成本太高，预期亏损
        assert result["profit_margin"] < 0
        assert result["risk_level"] == "high"  # 亏损 -> 高风险
        # 保本售价大于总成本（因为百分比成本会随售价变化）
        assert result["break_even_price"] > result["total_cost"]

    def test_high_profit_scenario(self):
        """高利润场景：低成本高售价"""
        result = calculate_profit(
            purchase_cost=10.0,
            selling_price=50.0,
            shipping_cost=3.0,
            amazon_fee_rate=0.15,
            fba_fee=2.0,
            ad_cost=1.0,
            return_rate=0.02,
        )

        # 验证利润率 >= 25%，应该是低风险
        assert result["profit_margin"] >= 25
        assert result["risk_level"] == "low"
        assert result["estimated_profit"] > 0

    def test_medium_profit_scenario(self):
        """中等利润场景：利润率在 10%-25% 之间"""
        # selling_price=30, purchase_cost=15, total fixed + percentage costs ≈ 25
        # profit_margin ≈ 16.7%, medium risk
        result = calculate_profit(
            purchase_cost=15.0,
            selling_price=30.0,
            shipping_cost=3.0,
            amazon_fee_rate=0.15,
            fba_fee=2.0,
            ad_cost=1.0,
            return_rate=0.03,
        )

        assert 10 <= result["profit_margin"] < 25
        assert result["risk_level"] == "medium"

    def test_low_profit_high_risk(self):
        """低利润高风险场景"""
        result = calculate_profit(
            purchase_cost=25.0,
            selling_price=30.0,
            shipping_cost=5.0,
            amazon_fee_rate=0.15,
            fba_fee=3.0,
            ad_cost=2.0,
            return_rate=0.05,
        )

        assert result["profit_margin"] < 10
        assert result["risk_level"] == "high"

    def test_zero_selling_price(self):
        """零售价边界：应该不会崩溃"""
        result = calculate_profit(
            purchase_cost=10.0,
            selling_price=0.0,
            shipping_cost=0.0,
            amazon_fee_rate=0.15,
            fba_fee=0.0,
            ad_cost=0.0,
            return_rate=0.0,
        )

        # 售价为 0，gross_revenue = 0
        assert result["gross_revenue"] == 0.0
        # 利润率为 0（除数保护）
        assert result["profit_margin"] == 0.0

    def test_high_return_rate_impact(self):
        """高退货率应该显著增加总成本"""
        result_low_return = calculate_profit(
            purchase_cost=20.0,
            selling_price=40.0,
            shipping_cost=5.0,
            return_rate=0.01,  # 1%
        )
        result_high_return = calculate_profit(
            purchase_cost=20.0,
            selling_price=40.0,
            shipping_cost=5.0,
            return_rate=0.10,  # 10%
        )

        # 高退货率 -> 总成本更高 -> 利润更低
        assert result_high_return["total_cost"] > result_low_return["total_cost"]
        assert result_high_return["estimated_profit"] < result_low_return["estimated_profit"]

    def test_break_even_price_correctness(self):
        """保本售价 = 总成本，卖这个价利润为0"""
        result = calculate_profit(
            purchase_cost=20.0,
            selling_price=40.0,
            shipping_cost=5.0,
            amazon_fee_rate=0.15,
            fba_fee=3.0,
            ad_cost=2.0,
            return_rate=0.03,
        )

        # 用保本售价再算一次，应该刚好不亏不赚（利润≈0）
        break_even_result = calculate_profit(
            purchase_cost=20.0,
            selling_price=result["break_even_price"],
            shipping_cost=5.0,
            amazon_fee_rate=0.15,
            fba_fee=3.0,
            ad_cost=2.0,
            return_rate=0.03,
        )

        assert abs(break_even_result["estimated_profit"]) < 0.01  # 利润几乎为0

    def test_risk_level_boundaries(self):
        """测试风险等级边界值"""
        # 刚好 25% -> low
        r1 = calculate_profit(purchase_cost=30, selling_price=40, shipping_cost=0,
                              amazon_fee_rate=0, fba_fee=0, ad_cost=0, return_rate=0)
        assert r1["profit_margin"] == 25.0
        assert r1["risk_level"] == "low"

        # 刚好 10% -> medium
        r2 = calculate_profit(purchase_cost=36, selling_price=40, shipping_cost=0,
                              amazon_fee_rate=0, fba_fee=0, ad_cost=0, return_rate=0)
        assert r2["profit_margin"] == 10.0
        assert r2["risk_level"] == "medium"

        # 低于 10% -> high
        r3 = calculate_profit(purchase_cost=37, selling_price=40, shipping_cost=0,
                              amazon_fee_rate=0, fba_fee=0, ad_cost=0, return_rate=0)
        assert r3["profit_margin"] < 10
        assert r3["risk_level"] == "high"

    def test_result_keys_completeness(self):
        """验证返回结果包含所有必需字段"""
        result = calculate_profit(10.0, 20.0)

        required_keys = [
            "gross_revenue", "total_cost", "estimated_profit",
            "profit_margin", "break_even_price", "risk_level",
        ]
        for key in required_keys:
            assert key in result, f"缺少字段: {key}"

    def test_default_parameters(self):
        """验证默认参数下函数可以正常执行"""
        result = calculate_profit(purchase_cost=10.0, selling_price=20.0)

        assert result["gross_revenue"] == 20.0
        assert isinstance(result["estimated_profit"], float)
        assert isinstance(result["risk_level"], str)
        assert result["risk_level"] in ("low", "medium", "high")
