/**
 * POST /refund
 *
 * BUG 10: no auth middleware — anyone can refund any order
 *         → auth / missing_authorization_check / unknown
 */
import { Router, Request, Response } from "express";
import { processRefund } from "../services/refund";

export const refundRouter = Router();

// BUG 10: no requireAuth middleware
refundRouter.post("/", async (req: Request, res: Response) => {
  const { orderId, amount } = req.body;
  const result = await processRefund(orderId, amount);
  res.json({ refundId: result.id, status: "completed" });
});
