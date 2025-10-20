from datetime import timedelta
from typing import Any

import boto3

from app.core.config import get_settings


class StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            endpoint_url=str(settings.s3_endpoint_url) if settings.s3_endpoint_url else None,
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            use_ssl=settings.s3_use_ssl,
        )
        self.bucket = settings.s3_bucket

    def generate_presigned_upload(
        self, *, key: str, expires_in: int = int(timedelta(minutes=10).total_seconds())
    ) -> dict[str, Any]:
        fields = {"acl": "private"}
        conditions = [["eq", "$acl", "private"]]
        return self.client.generate_presigned_post(
            Bucket=self.bucket,
            Key=key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expires_in,
        )

    def build_object_url(self, key: str) -> str:
        settings = get_settings()
        if settings.s3_endpoint_url:
            return f"{settings.s3_endpoint_url}/{self.bucket}/{key}"
        return f"https://{self.bucket}.s3.{settings.s3_region}.amazonaws.com/{key}"
