"""
Products 路由 —— 商品管理 CRUD

提供商品列表、新增、编辑、删除功能。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.schemas import ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def product_list(request: Request, db: Session = Depends(get_db)):
    """商品列表页"""
    products = crud.get_products(db)
    return request.app.state.templates.TemplateResponse(
        "products.html",
        {"request": request, "title": "商品管理", "products": products},
    )


@router.get("/new")
async def product_form_new(request: Request):
    """新增商品表单页"""
    return request.app.state.templates.TemplateResponse(
        "product_form.html",
        {"request": request, "title": "新增商品", "product": None, "action": "create"},
    )


@router.get("/{product_id}/edit")
async def product_form_edit(request: Request, product_id: int, db: Session = Depends(get_db)):
    """编辑商品表单页"""
    product = crud.get_product(db, product_id)
    if not product:
        return RedirectResponse(url="/products", status_code=303)
    return request.app.state.templates.TemplateResponse(
        "product_form.html",
        {"request": request, "title": "编辑商品", "product": product, "action": "edit"},
    )


@router.post("/")
async def product_create(
    request: Request,
    form: Annotated[ProductCreate, Form()],
    db: Session = Depends(get_db),
):
    """创建商品（表单提交）"""
    crud.create_product(db, form.model_dump())
    return RedirectResponse(url="/products", status_code=303)


@router.post("/{product_id}/update")
async def product_update(
    request: Request,
    product_id: int,
    form: Annotated[ProductCreate, Form()],
    db: Session = Depends(get_db),
):
    """更新商品（表单提交）"""
    crud.update_product(db, product_id, form.model_dump())
    return RedirectResponse(url="/products", status_code=303)


@router.post("/{product_id}/delete")
async def product_delete(request: Request, product_id: int, db: Session = Depends(get_db)):
    """删除商品"""
    crud.delete_product(db, product_id)
    return RedirectResponse(url="/products", status_code=303)
