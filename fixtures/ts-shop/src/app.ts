/**
 * Express application entry point.
 */
import express from "express";
import { checkoutRouter } from "./routes/checkout";
import { refundRouter } from "./routes/refund";
import { productsRouter } from "./routes/products";
import { uploadRouter } from "./routes/upload";
import { shippingRouter } from "./routes/shipping";
import { adminRouter } from "./routes/admin";

const app = express();
app.use(express.json());

app.use("/checkout", checkoutRouter);
app.use("/refund", refundRouter);
app.use("/products", productsRouter);
app.use("/upload-avatar", uploadRouter);
app.use("/shipping-rates", shippingRouter);
app.use("/admin", adminRouter);

export default app;
