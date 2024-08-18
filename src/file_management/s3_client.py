from fastapi import UploadFile
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from contextlib import asynccontextmanager

from config import settings


class S3Client:
    config = {
        "aws_access_key_id": settings.s3_access_key.get_secret_value(),
        "aws_secret_access_key": settings.s3_secret_key.get_secret_value(),
        "endpoint_url": settings.s3_endpoint_url,
    }
    bucket_name = settings.s3_bucket_name

    def __init__(self):
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile, file_name: str) -> None:
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=file,
                )
        except ClientError as e:
            print(f"Error uploading file: {e}")

s3_client = S3Client()
