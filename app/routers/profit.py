"""
Profit Calculator 路由 —— 利润计算器

Amazon 选品中最核心的分析工具。
输入成本参数，计算利润、利润率、保本售价、风险等级。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.services.profit_service import calculate_profit
from app.schemas import ProfitCalculateRequest
from app.config import settings

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
            "default_exchange_rate": settings.usd_cny_rate,
        },
    )


@router.post("/calculate")
async def profit_calculate(
    request: Request,
    form: Annotated[ProfitCalculateRequest, Form()],
    db: Session = Depends(get_db),
):
    """执行利润计算并保存记录"""
    # 调用 service 层的计算函数
    result = calculate_profit(
        purchase_cost=form.purchase_cost,
        selling_price=form.selling_price,
        shipping_cost=form.shipping_cost,
        amazon_fee_rate=form.amazon_fee_rate,
        fba_fee=form.fba_fee,
        ad_cost=form.ad_cost,
        return_rate=form.return_rate,
        exchange_rate=form.exchange_rate,
    )

    # 保存到数据库
    crud.create_profit_record(db, {
        "product_name": form.product_name,
        "purchase_cost": form.purchase_cost,
        "selling_price": form.selling_price,
        "shipping_cost": form.shipping_cost,
        "amazon_fee_rate": form.amazon_fee_rate,
        "fba_fee": form.fba_fee,
        "ad_cost": form.ad_cost,
        "return_rate": form.return_rate,
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
                **form.model_dump(),
                **result,
            },
            "default_exchange_rate": settings.usd_cny_rate,
        },
    )


@router.post("/{record_id}/delete")
async def profit_delete(request: Request, record_id: int, db: Session = Depends(get_db)):
    """删除利润记录"""
    crud.delete_profit_record(db, record_id)
    return RedirectResponse(url="/profit", status_code=303)
