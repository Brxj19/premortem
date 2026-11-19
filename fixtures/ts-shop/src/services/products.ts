/**
 * Product listing and cart.
 *
 * BUG 5: Redis get with no try — Redis down crashes the product list
 *        → cache:redis / unavailable / unhandled_in_code
 * BUG 6: Cache used as the only store for cart totals
 *        → cache / cache_as_source_of_truth / unknown
 */
import Redis from "ioredis";
import { prisma } from "../db";
import { config } from "../config";

const redis = new Redis(config.redisUrl);

export async function listProducts() {
  // BUG 5: no try/catch — if Redis is down, this crashes the entire endpoint
  const cached = await redis.get("products:all");
  if (cached) {
    return JSON.parse(cached);
  }

  const products = await prisma.product.findMany();
  await redis.setex("products:all", 300, JSON.stringify(products));
  return products;
}

export async function getCartTotal(userId: number): Promise<number> {
  // BUG 6: cart total lives only in Redis — if Redis flushes or is down,
  // the cart total is lost with no DB backup
  const raw = await redis.get(`cart:total:${userId}`);
  return raw ? parseFloat(raw) : 0;
}

export async function updateCartTotal(userId: number, total: number) {
  await redis.set(`cart:total:${userId}`, total.toString());
}
