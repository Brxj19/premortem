"""Shipping rate lookups.

CONTROL: HTTP call with timeout, retry decorator, and logged except
         → handled for timeout, server_error, rate_limited
"""
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

client = httpx.Client(timeout=10)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
def get_rates(origin_zip: str, dest_zip: str, weight_kg: float) -> list:
    try:
        resp = client.post(
            "https://api.shipping-provider.com/v1/rates",
            json={"origin": origin_zip, "dest": dest_zip, "weight": weight_kg},
        )
        resp.raise_for_status()
        return resp.json()["rates"]
    except httpx.HTTPStatusError as e:
        logger.error("Shipping API error %s: %s", e.response.status_code, e)
        raise
    except httpx.TimeoutException as e:
        logger.error("Shipping API timeout: %s", e)
        raise
