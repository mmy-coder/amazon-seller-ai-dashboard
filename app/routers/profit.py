"""
Profit Calculator 路由 —— 利润计算器

Amazon 选品中最核心的分析工具。
输入成本参数，计算利润、利润率、保本售价、风险等级。
"""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.services.profit_service import calculate_profit

router = APIRouter(prefix="/profit", tags=["Profit Calculator"])


@router.get("/")
async def profit_page(request: Request, db: Session = Depends(get_db)):
    """利润计算器首页"""
    records = crud.get_profit_records(db)
    return request.app.state.templates.TemplateResponse(
        "profit.html",
        {
            "request": request,
            "title": "利润计算器",
            "records": records,
            "result": None,
        },
    )


@router.post("/calculate")
async def profit_calculate(
    request: Request,
    product_name: str = Form(...),
    purchase_cost: float = Form(...),
    selling_price: float = Form(...),
    shipping_cost: float = Form(0.0),
    amazon_fee_rate: float = Form(0.15),
    fba_fee: float = Form(0.0),
    ad_cost: float = Form(0.0),
    return_rate: float = Form(0.03),
    db: Session = Depends(get_db),
):
    """执行利润计算并保存记录"""
    # 调用 service 层的计算函数
    result = calculate_profit(
        purchase_cost=purchase_cost,
        selling_price=selling_price,
        shipping_cost=shipping_cost,
        amazon_fee_rate=amazon_fee_rate,
        fba_fee=fba_fee,
        ad_cost=ad_cost,
        return_rate=return_rate,
    )

    # 保存到数据库
    crud.create_profit_record(db, {
        "product_name": product_name,
        "purchase_cost": purchase_cost,
        "selling_price": selling_price,
        "shipping_cost": shipping_cost,
        "amazon_fee_rate": amazon_fee_rate,
        "fba_fee": fba_fee,
        "ad_cost": ad_cost,
        "return_rate": return_rate,
        "gross_revenue": result["gross_revenue"],
        "total_cost": result["total_cost"],
        "estimated_profit": result["estimated_profit"],
        "profit_margin": result["profit_margin"],
        "break_even_price": result["break_even_price"],
        "risk_level": result["risk_level"],
    })

    records = crud.get_profit_records(db)
    return request.app.state.templates.TemplateResponse(
        "profit.html",
        {
            "request": request,
            "title": "利润计算器",
            "records": records,
            "result": {
                "product_name": product_name,
                "purchase_cost": purchase_cost,
                "selling_price": selling_price,
                "shipping_cost": shipping_cost,
                "amazon_fee_rate": amazon_fee_rate,
                "fba_fee": fba_fee,
                "ad_cost": ad_cost,
                "return_rate": return_rate,
                **result,
            },
        },
    )


@router.get("/{record_id}/delete")
async def profit_delete(request: Request, record_id: int, db: Session = Depends(get_db)):
    """删除利润记录"""
    crud.delete_profit_record(db, record_id)
    return RedirectResponse(url="/profit", status_code=303)
