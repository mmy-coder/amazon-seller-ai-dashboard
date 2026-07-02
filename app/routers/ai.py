"""
AI 路由 —— AI 评论分析和 Listing 优化

两个核心 AI 功能：
1. 评论分析：从用户评论中提取洞察
2. Listing 优化：基于商品信息生成优化的 Listing 内容

都支持：有 API Key 时调用 DeepSeek，没有时使用 Mock 数据。
"""

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_service import analyze_reviews, optimize_listing

router = APIRouter(prefix="/ai", tags=["AI Tools"])


@router.get("/reviews")
async def review_analysis_page(request: Request):
    """AI 评论分析页面"""
    return request.app.state.templates.TemplateResponse(
        "review_analysis.html",
        {"request": request, "title": "AI 评论分析", "result": None},
    )


@router.post("/reviews/analyze")
async def review_analysis_run(
    request: Request,
    reviews: str = Form(...),
    db: Session = Depends(get_db),
):
    """执行 AI 评论分析"""
    result = await analyze_reviews(reviews)
    return request.app.state.templates.TemplateResponse(
        "review_analysis.html",
        {
            "request": request,
            "title": "AI 评论分析",
            "result": result,
            "reviews": reviews,
        },
    )


@router.get("/listing-optimizer")
async def listing_optimizer_page(request: Request):
    """AI Listing 优化页面"""
    return request.app.state.templates.TemplateResponse(
        "listing_optimizer.html",
        {"request": request, "title": "AI Listing 优化", "result": None},
    )


@router.post("/listing-optimizer/optimize")
async def listing_optimizer_run(
    request: Request,
    product_name: str = Form(...),
    category: str = Form(""),
    core_selling_points: str = Form(""),
    target_users: str = Form(""),
    competitor_weakness: str = Form(""),
    user_pain_points: str = Form(""),
    db: Session = Depends(get_db),
):
    """执行 AI Listing 优化"""
    result = await optimize_listing(
        product_name=product_name,
        category=category,
        core_selling_points=core_selling_points,
        target_users=target_users,
        competitor_weakness=competitor_weakness,
        user_pain_points=user_pain_points,
    )
    return request.app.state.templates.TemplateResponse(
        "listing_optimizer.html",
        {
            "request": request,
            "title": "AI Listing 优化",
            "result": result,
        },
    )
