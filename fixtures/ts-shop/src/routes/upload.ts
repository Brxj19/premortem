/**
 * POST /upload-avatar
 */
import { Router, Request, Response } from "express";
import multer from "multer";
import { requireAuth } from "../auth";
import { uploadAvatar } from "../services/upload";

const upload = multer();

export const uploadRouter = Router();

uploadRouter.post(
  "/",
  requireAuth,
  upload.single("file"),
  async (req: Request, res: Response) => {
    const user = (req as any).user;
    const file = (req as any).file!;
    const record = await uploadAvatar(user.userId, file.originalname, file.buffer);
    res.json({ uploadId: record.id, s3Key: record.s3Key });
  }
);
