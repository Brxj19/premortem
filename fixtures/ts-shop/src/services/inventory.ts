/**
 * Inventory management.
 *
 * CONTROL: DB transaction around two writes → handled for
 *          multi_write_without_transaction.
 */
import { prisma } from "../db";

export async function transferStock(
  fromProductId: number,
  toProductId: number,
  quantity: number
) {
  await prisma.$transaction(async (tx) => {
    const source = await tx.product.findUnique({ where: { id: fromProductId } });
    const dest = await tx.product.findUnique({ where: { id: toProductId } });
    if (!source || !dest) {
      throw new Error("Product not found");
    }
    if (source.stock < quantity) {
      throw new Error("Insufficient stock");
    }
    await tx.product.update({
      where: { id: fromProductId },
      data: { stock: { decrement: quantity } },
    });
    await tx.product.update({
      where: { id: toProductId },
      data: { stock: { increment: quantity } },
    });
    console.log(`Transferred ${quantity} from product ${fromProductId} to ${toProductId}`);
  });
}
