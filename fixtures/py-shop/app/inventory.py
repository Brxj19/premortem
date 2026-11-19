"""Inventory management.

CONTROL: DB transaction block around two writes → handled for
         multi_write_without_transaction.
"""
import logging

from sqlalchemy.orm import Session

from app.models import Product

logger = logging.getLogger(__name__)


def transfer_stock(db: Session, from_product_id: int, to_product_id: int, quantity: int):
    with db.begin():
        source = db.query(Product).filter(Product.id == from_product_id).with_for_update().first()
        dest = db.query(Product).filter(Product.id == to_product_id).with_for_update().first()
        if not source or not dest:
            raise ValueError("Product not found")
        if source.stock < quantity:
            raise ValueError("Insufficient stock")
        source.stock -= quantity
        dest.stock += quantity
        logger.info("Transferred %d from product %d to %d", quantity, from_product_id, to_product_id)
