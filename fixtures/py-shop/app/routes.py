"""API routes.

BUG 10: POST /refund has no auth dependency
        → auth / missing_authorization_check / unknown
BUG 11: POST /checkout body parsed with no schema validation
        → user_input / missing_validation / unknown

CONTROL: GET /admin/products has auth dependency and Pydantic body
         → handled for missing_authorization_check and missing_validation
"""
import logging

from fastapi import APIRouter, Depends, Request, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.pay import charge_customer
from app.refund import process_refund
from app.products import list_products
from app.upload import upload_avatar
from app.email_service import send_order_confirmation
from app.shipping import get_rates

logger = logging.getLogger(__name__)
router = APIRouter()


class AdminProductUpdate(BaseModel):
    name: str
    price: float
    stock: int


@router.post("/checkout")
async def checkout(request: Request, db: Session = Depends(get_db)):
    # BUG 11: raw dict from request body — no Pydantic model, no validation
    body = await request.json()
    email = body["email"]
    amount = body["amount"]

    order = charge_customer(db, email, amount)
    send_order_confirmation(email, order.id)
    return {"order_id": order.id, "status": "paid"}


@router.post("/refund")
def refund(order_id: int, amount: float, db: Session = Depends(get_db)):
    # BUG 10: no auth dependency — anyone can refund any order
    result = process_refund(db, order_id, amount)
    return {"refund_id": result.id, "status": "completed"}


@router.get("/products")
def products(db: Session = Depends(get_db)):
    return list_products(db)


@router.post("/upload-avatar")
def upload(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = file.file.read()
    record = upload_avatar(db, user["user_id"], file.filename, data)
    return {"upload_id": record.id, "s3_key": record.s3_key}


@router.get("/shipping-rates")
def shipping_rates(origin: str, dest: str, weight: float):
    rates = get_rates(origin, dest, weight)
    return {"rates": rates}


# CONTROL: auth dependency + Pydantic model validation → handled
@router.put("/admin/products/{product_id}")
def update_product(
    product_id: int,
    body: AdminProductUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"error": "not found"}, 404
    product.name = body.name
    product.price = body.price
    product.stock = body.stock
    db.commit()
    return {"id": product.id, "name": product.name}
