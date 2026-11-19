"""Refund processing.

BUG 4: Two DB writes in refund flow without a transaction
       → database / multi_write_without_transaction / unhandled_in_code
"""
import logging

import stripe
from sqlalchemy.orm import Session

from app.models import Order, Refund

logger = logging.getLogger(__name__)


def process_refund(db: Session, order_id: int, amount: float):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError(f"Order {order_id} not found")

    refund = stripe.Refund.create(
        charge=order.stripe_charge_id,
        amount=int(amount * 100),
    )
    logger.info("Stripe refund created: %s", refund.id)

    # BUG 4: two separate writes without a transaction — if the second fails,
    # the refund record exists but the order status is stale
    refund_record = Refund(
        order_id=order_id,
        amount=amount,
        status="completed",
    )
    db.add(refund_record)
    db.commit()

    order.status = "refunded"
    db.commit()

    return refund_record
