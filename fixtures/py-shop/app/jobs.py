"""Background tasks.

BUG 3: except: pass around inventory update → silent handler
       → database / multi_write_without_transaction (swallowed)
BUG 7: Queue consumer with no dedup on order id
       → queue / duplicate_delivery / unhandled_in_code
"""
import json
import logging

from celery import Celery
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Product, Order

logger = logging.getLogger(__name__)

app = Celery("shop", broker="redis://localhost:6379/1")


@app.task
def sync_inventory(product_id: int, quantity_sold: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock -= quantity_sold
            db.commit()
    except:
        # BUG 3: bare except with pass — inventory update failure is completely silent
        pass
    finally:
        db.close()


@app.task
def process_order_from_queue(message_body: str):
    # BUG 7: no deduplication — if the message is delivered twice,
    # the order is processed twice
    data = json.loads(message_body)
    order_id = data["order_id"]

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order and order.status == "pending":
            order.status = "processing"
            db.commit()
            logger.info("Processing order %s", order_id)
    finally:
        db.close()
