from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileMetadata(Base):
    __tablename__ = 'file_metadata'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    file_format = Column(String, nullable=False)
    file_size = Column(Float, nullable=False)
    extension = Column(String, nullable=False)
