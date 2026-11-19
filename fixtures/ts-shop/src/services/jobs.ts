/**
 * Background jobs.
 *
 * BUG 3: empty catch around inventory update → silent handler
 *        → database / multi_write_without_transaction (swallowed)
 * BUG 7: Queue consumer with no dedup on order id
 *        → queue / duplicate_delivery / unhandled_in_code
 */
import { Worker } from "bullmq";
import { prisma } from "../db";

// BUG 3: inventory sync with swallowed error
export async function syncInventory(productId: number, quantitySold: number) {
  try {
    await prisma.product.update({
      where: { id: productId },
      data: { stock: { decrement: quantitySold } },
    });
  } catch {
    // empty catch — inventory failure is completely silent
  }
}

// BUG 7: order consumer with no deduplication
const orderWorker = new Worker("orders", async (job) => {
  const { orderId } = job.data;

  // No check if this orderId was already processed — duplicate delivery
  // processes the order twice
  const order = await prisma.order.findUnique({ where: { id: orderId } });
  if (order && order.status === "pending") {
    await prisma.order.update({
      where: { id: orderId },
      data: { status: "processing" },
    });
    console.log("Processing order", orderId);
  }
});

export { orderWorker };
