/**
 * GET /shipping-rates
 */
import { Router, Request, Response } from "express";
import { getRates } from "../services/shipping";

export const shippingRouter = Router();

shippingRouter.get("/", async (req: Request, res: Response) => {
  const { origin, dest, weight } = req.query;
  const rates = await getRates(
    origin as string,
    dest as string,
    parseFloat(weight as string)
  );
  res.json({ rates });
});
