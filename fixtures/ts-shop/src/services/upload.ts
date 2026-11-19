/**
 * File upload handling.
 *
 * BUG 8: S3 upload with no size check, DB row written first
 *        → storage / size_limit / unhandled_in_code
 *        → storage / orphaned_object
 */
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { prisma } from "../db";
import { config } from "../config";

const s3 = new S3Client({ region: "us-east-1" });

export async function uploadAvatar(userId: number, filename: string, fileData: Buffer) {
  const s3Key = `avatars/${userId}/${filename}`;

  // BUG 8: DB row is written first — if the S3 upload fails afterward,
  // we have an orphaned DB record. Also no size check on fileData.
  const uploadRecord = await prisma.upload.create({
    data: {
      userId,
      s3Key,
      filename,
    },
  });

  await s3.send(
    new PutObjectCommand({
      Bucket: config.s3Bucket,
      Key: s3Key,
      Body: fileData,
    })
  );

  return uploadRecord;
}
