from pydantic import BaseModel
from typing import List, Optional, Any

class FileUploadRequest(BaseModel):
    file_path: str

class FolderUploadRequest(BaseModel):
    folder_path: str

class DataIngestionResponse(BaseModel):
    status: str
    message: str
    result: Optional[Any] = None
