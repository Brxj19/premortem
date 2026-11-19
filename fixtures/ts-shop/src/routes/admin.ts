/**
 * Admin routes.
 *
 * CONTROL: auth middleware + Zod validation → handled for
 *          missing_authorization_check and missing_validation.
 */
import { Router, Request, Response } from "express";
import { z } from "zod";
import { requireAuth } from "../auth";
import { prisma } from "../db";

export const adminRouter = Router();

const ProductUpdateSchema = z.object({
  name: z.string(),
  price: z.number().positive(),
  stock: z.number().int().nonneg(),
});

adminRouter.put(
  "/products/:id",
  requireAuth,
  async (req: Request, res: Response) => {
    const parsed = ProductUpdateSchema.parse(req.body);
    const product = await prisma.product.update({
      where: { id: parseInt(req.params.id as string) },
      data: parsed,
    });
    res.json({ id: product.id, name: product.name });
  }
);
