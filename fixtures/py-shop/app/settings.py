"""Application settings.

CONTROL: config read with a default value → handled for missing_variable.
"""
import os


DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/shop")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
S3_BUCKET = os.environ.get("S3_BUCKET", "shop-uploads")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
