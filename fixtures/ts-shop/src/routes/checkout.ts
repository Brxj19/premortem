/**
 * POST /checkout
 *
 * BUG 11: request body parsed with no schema validation (no Zod, no express-validator)
 *         → user_input / missing_validation / unknown
 */
import { Router, Request, Response } from "express";
import { chargeCustomer } from "../services/payment";
import { sendOrderConfirmation } from "../services/email";

export const checkoutRouter = Router();

checkoutRouter.post("/", async (req: Request, res: Response) => {
  // BUG 11: raw body — no Zod schema, no express-validator
  const { email, amount } = req.body;

  const order = await chargeCustomer(email, amount);
  await sendOrderConfirmation(email, order.id);
  res.json({ orderId: order.id, status: "paid" });
});
