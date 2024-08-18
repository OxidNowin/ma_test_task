from aiofiles import open as aio_open
from fastapi import UploadFile

from config import settings

import os
import uuid


def generate_uid() -> str:
    return str(uuid.uuid4())


async def save_file_locally(file: UploadFile, uid: str) -> None:
    file_extension = file.filename.split('.')[-1]
    file_path = f"{settings.MEDIA_DIR}/{uid}.{file_extension}"

    os.makedirs(settings.MEDIA_DIR, exist_ok=True)

    async with aio_open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
