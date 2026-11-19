/**
 * Refund processing.
 *
 * BUG 4: Two DB writes in refund flow without a transaction
 *        → database / multi_write_without_transaction / unhandled_in_code
 */
import Stripe from "stripe";
import { prisma } from "../db";

const stripe = new Stripe(process.env.STRIPE_SECRET || "", { apiVersion: "2023-10-16" });

export async function processRefund(orderId: number, amount: number) {
  const order = await prisma.order.findUnique({ where: { id: orderId } });
  if (!order) {
    throw new Error(`Order ${orderId} not found`);
  }

  const refund = await stripe.refunds.create({
    charge: order.stripeChargeId,
    amount: Math.round(amount * 100),
  });
  console.log("Stripe refund created:", refund.id);

  // BUG 4: two separate writes without a transaction — if the second fails,
  // the refund record exists but the order status is stale
  const refundRecord = await prisma.refund.create({
    data: {
      orderId,
      amount,
      status: "completed",
    },
  });

  await prisma.order.update({
    where: { id: orderId },
    data: { status: "refunded" },
  });

  return refundRecord;
}
