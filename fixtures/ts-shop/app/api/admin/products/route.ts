/**
 * Next.js API route: PUT /api/admin/products
 *
 * CONTROL: Zod validation + auth check in a Next.js route handler
 *          → handled for missing_authorization_check and missing_validation
 */
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { prisma } from "../../../../src/db";

const UpdateSchema = z.object({
  name: z.string(),
  price: z.number().positive(),
  stock: z.number().int().nonneg(),
});

export async function PUT(req: NextRequest) {
  const authHeader = req.headers.get("authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await req.json();
  const parsed = UpdateSchema.parse(body);

  const product = await prisma.product.update({
    where: { id: 1 },
    data: parsed,
  });

  return NextResponse.json({ id: product.id, name: product.name });
}
