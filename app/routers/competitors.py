"""
Competitors 路由 —— 竞品分析管理

竞品分析是 Amazon 运营的核心环节之一。
通过分析竞品的价格、卖点、弱点，找到自己的差异化方向。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.schemas import CompetitorCreate

router = APIRouter(prefix="/competitors", tags=["Competitors"])


@router.get("/")
async def competitor_list(request: Request, db: Session = Depends(get_db)):
    """竞品列表页"""
    competitors = crud.get_competitors(db)
    products = crud.get_products(db)
    return request.app.state.templates.TemplateResponse(
        "competitors.html",
        {
            "request": request,
            "title": "竞品分析",
            "competitors": competitors,
            "products": products,
        },
    )


@router.get("/new")
async def competitor_form_new(request: Request, db: Session = Depends(get_db)):
    """新增竞品表单页"""
    products = crud.get_products(db)
    return request.app.state.templates.TemplateResponse(
        "competitor_form.html",
        {
            "request": request,
            "title": "新增竞品",
            "competitor": None,
            "products": products,
            "action": "create",
        },
    )


@router.get("/{competitor_id}/edit")
async def competitor_form_edit(request: Request, competitor_id: int, db: Session = Depends(get_db)):
    """编辑竞品表单页"""
    competitor = crud.get_competitor(db, competitor_id)
    if not competitor:
        return RedirectResponse(url="/competitors", status_code=303)
    products = crud.get_products(db)
    return request.app.state.templates.TemplateResponse(
        "competitor_form.html",
        {
            "request": request,
            "title": "编辑竞品",
            "competitor": competitor,
            "products": products,
            "action": "edit",
        },
    )


@router.post("/")
async def competitor_create(
    request: Request,
    form: Annotated[CompetitorCreate, Form()],
    db: Session = Depends(get_db),
):
    """创建竞品"""
    crud.create_competitor(db, form.model_dump())
    return RedirectResponse(url="/competitors", status_code=303)


@router.post("/{competitor_id}/update")
async def competitor_update(
    request: Request,
    competitor_id: int,
    form: Annotated[CompetitorCreate, Form()],
    db: Session = Depends(get_db),
):
    """更新竞品"""
    crud.update_competitor(db, competitor_id, form.model_dump())
    return RedirectResponse(url="/competitors", status_code=303)


@router.post("/{competitor_id}/delete")
async def competitor_delete(request: Request, competitor_id: int, db: Session = Depends(get_db)):
    """删除竞品"""
    crud.delete_competitor(db, competitor_id)
    return RedirectResponse(url="/competitors", status_code=303)
