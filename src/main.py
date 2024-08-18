from fastapi import FastAPI

from file_management.router import router as fm_router
from database import (
    Base,
    engine
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(fm_router, prefix="/file_management/")
