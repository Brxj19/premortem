/**
 * Payment processing.
 *
 * BUG 1: Stripe charge with no timeout → http_api:stripe / timeout / unhandled_in_code
 * BUG 2: Charge then order insert with no idempotency key or compensation
 *        → http_api:stripe / partial_success / unhandled_in_code
 * BUG 9: process.env.STRIPE_KEY read inside request handler
 *        → config / missing_variable / unhandled_in_code
 */
import Stripe from "stripe";
import { prisma } from "../db";

export async function chargeCustomer(email: string, amount: number) {
  // BUG 9: bare process.env read — crashes if STRIPE_KEY is missing
  const stripe = new Stripe(process.env.STRIPE_KEY!, { apiVersion: "2023-10-16" });

  // BUG 1: no timeout on Stripe call
  // BUG 2: charge succeeds, then insert could fail — no idempotency key
  let charge: Stripe.Charge;
  try {
    charge = await stripe.charges.create({
      amount,
      currency: "usd",
      source: "tok_visa",
      description: `Order for ${email}`,
    });
  } catch (err: any) {
    if (err.type === "StripeCardError") {
      console.error("Card declined:", err.message);
      throw err;
    }
    throw err;
  }

  // If this insert fails, the customer is charged but has no order record
  const order = await prisma.order.create({
    data: {
      customerEmail: email,
      total: amount / 100,
      stripeChargeId: charge.id,
      status: "paid",
    },
  });

  return order;
}
