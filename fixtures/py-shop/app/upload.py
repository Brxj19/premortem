"""File upload handling.

BUG 8: S3 upload with no size check, DB row written first
       → storage / size_limit / unhandled_in_code
       → storage / orphaned_object (DB row exists but upload may fail)
"""
import logging

import boto3
from sqlalchemy.orm import Session

from app.models import Upload
from app.settings import S3_BUCKET

logger = logging.getLogger(__name__)

s3 = boto3.client("s3")


def upload_avatar(db: Session, user_id: int, filename: str, file_data: bytes):
    s3_key = f"avatars/{user_id}/{filename}"

    # BUG 8: DB row is written first — if the S3 upload fails afterward,
    # we have an orphaned DB record pointing to a nonexistent object.
    # Also no size check on file_data.
    upload_record = Upload(
        user_id=user_id,
        s3_key=s3_key,
        filename=filename,
    )
    db.add(upload_record)
    db.commit()

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=file_data,
    )

    return upload_record
