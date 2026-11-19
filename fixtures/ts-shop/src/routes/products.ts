/**
 * GET /products
 */
import { Router, Request, Response } from "express";
import { listProducts } from "../services/products";

export const productsRouter = Router();

productsRouter.get("/", async (_req: Request, res: Response) => {
  const products = await listProducts();
  res.json(products);
});
