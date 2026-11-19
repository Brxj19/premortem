"""Payment processing.

BUG 1: Stripe charge with no timeout → http_api:stripe / timeout / unhandled_in_code
BUG 2: Charge then order insert with no idempotency key or compensation
       → http_api:stripe / partial_success / unhandled_in_code
BUG 9: os.environ["STRIPE_KEY"] read inside request handler
       → config / missing_variable / unhandled_in_code
"""
import os
import logging

import stripe
from sqlalchemy.orm import Session

from app.models import Order

logger = logging.getLogger(__name__)


def charge_customer(db: Session, email: str, amount: int, currency: str = "usd"):
    # BUG 9: bare os.environ read — crashes if STRIPE_KEY is missing
    stripe.api_key = os.environ["STRIPE_KEY"]

    # BUG 1: no timeout on Stripe call
    # BUG 2: charge succeeds, then insert could fail — no idempotency key,
    #         no compensation (refund) if the insert fails
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source="tok_visa",
            description=f"Order for {email}",
        )
    except stripe.error.CardError as e:
        logger.error("Card declined: %s", e)
        raise

    # If this insert fails, the customer is charged but has no order record
    order = Order(
        customer_email=email,
        total=amount / 100,
        stripe_charge_id=charge.id,
        status="paid",
    )
    db.add(order)
    db.commit()
    return order
