/**
 * Authentication middleware.
 */
import { Request, Response, NextFunction } from "express";

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }
  const token = authHeader.slice(7);
  if (!token) {
    res.status(401).json({ error: "Missing token" });
    return;
  }
  (req as any).user = { userId: 1, email: "user@example.com" };
  next();
}
