/**
 * Application configuration.
 *
 * CONTROL: config reads with defaults → handled for missing_variable.
 */
export const config = {
  databaseUrl: process.env.DATABASE_URL || "postgresql://localhost:5432/shop",
  redisUrl: process.env.REDIS_URL || "redis://localhost:6379/0",
  s3Bucket: process.env.S3_BUCKET || "shop-uploads",
  sendgridApiKey: process.env.SENDGRID_API_KEY || "",
  logLevel: process.env.LOG_LEVEL || "info",
};
