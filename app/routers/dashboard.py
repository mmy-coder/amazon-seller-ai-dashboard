"""
Dashboard 路由 —— 首页数据看板

展示运营关键指标，是卖家每天打开后台看到的第一页。
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """首页 Dashboard"""
    stats = crud.get_dashboard_stats(db)
    recent_products = crud.get_recent_products(db, limit=5)
    status_dist = crud.get_product_status_distribution(db)
    category_dist = crud.get_product_category_distribution(db)
    recent_profits = crud.get_recent_profit_records(db, limit=5)

    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Dashboard",
            "stats": stats,
            "recent_products": recent_products,
            "status_dist": status_dist,
            "category_dist": category_dist,
            "recent_profits": recent_profits,
        },
    )
