"""Product listing.

BUG 5: Redis get with no try — Redis down crashes the product list
       → cache:redis / unavailable / unhandled_in_code
BUG 6: Cache used as the only store for cart totals
       → cache / cache_as_source_of_truth / unknown
"""
import json

import redis
from sqlalchemy.orm import Session

from app.models import Product
from app.settings import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)


def list_products(db: Session):
    # BUG 5: no try/except — if Redis is down, this crashes the entire endpoint
    cached = r.get("products:all")
    if cached:
        return json.loads(cached)

    products = db.query(Product).all()
    result = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    r.setex("products:all", 300, json.dumps(result))
    return result


def get_cart_total(user_id: int) -> float:
    # BUG 6: cart total lives only in Redis — if Redis flushes or is down,
    # the cart total is lost with no DB backup
    raw = r.get(f"cart:total:{user_id}")
    if raw is None:
        return 0.0
    return float(raw)


def update_cart_total(user_id: int, total: float):
    r.set(f"cart:total:{user_id}", str(total))
