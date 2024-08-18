from fastapi import UploadFile

from file_management.s3_client import s3_client
from celery_config import app
from config import settings

import os


@app.task
async def upload_to_cloud(file: UploadFile, uid: str):
    await s3_client.upload_file(file, uid)


@app.task
def cleanup_files():
    for filename in os.listdir(settings.MEDIA_DIR):
        file_path = os.path.join(settings.MEDIA_DIR, filename)
        os.remove(file_path)
