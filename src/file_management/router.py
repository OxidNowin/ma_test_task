from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

from models import FileMetadata
from database import get_db
from utils import save_file_locally, generate_uid
from tasks.tasks import upload_to_cloud

from config import settings

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    uid = generate_uid()
    await save_file_locally(file, uid)

    file_metadata = FileMetadata(
        uid=uid,
        original_filename=file.filename,
        file_format=file.content_type,
        file_size=len(await file.read()),
        extension=file.filename.split('.')[-1]
    )

    db.add(file_metadata)
    db.commit()

    upload_to_cloud.delay(file.file, uid)

    return {"uid": uid, "filename": file.filename}


@router.get("/file/{uid}")
async def get_file(uid: str, db: Session = Depends(get_db)):
    file_metadata = db.query(FileMetadata).filter(FileMetadata.uid == uid).first()
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"{settings.MEDIA_DIR}/{uid}.{file_metadata.extension}"
    return {"file_path": file_path}
