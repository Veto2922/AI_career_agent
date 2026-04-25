from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.api_routes.apis_schemas.data_ingestion_schemas import (
    FileUploadRequest,
    FolderUploadRequest,
    DataIngestionResponse,
)
from src.data_ingestion_block.data_ingestion import DataIngestion
from loguru import logger
import os

router = APIRouter(prefix="/data-ingestion", tags=["Data Ingestion"])


data_ingestion_service = DataIngestion()


# Dependency-like retrieval of the service
def get_data_ingestion_service():
    return data_ingestion_service


@router.post("/upload-file", response_model=DataIngestionResponse)
async def upload_file(request: FileUploadRequest):
    logger.info(f"Received request to upload file: {request.file_path}")
    if not os.path.exists(request.file_path):
        logger.error(f"File not found: {request.file_path}")
        raise HTTPException(status_code=404, detail="File not found")

    try:
        service = get_data_ingestion_service()
        result = service.upload_file(request.file_path)

        logger.info(f"Successfully uploaded file: {request.file_path}")
        return {
            "status": "success",
            "message": f"File {request.file_path} uploaded successfully",
            "result": result,
        }

    except Exception as e:
        logger.error(f"Error uploading file {request.file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-folder", response_model=DataIngestionResponse)
async def upload_folder(request: FolderUploadRequest):
    """
    Upload all PDF files in a folder to PageIndex.
    """
    logger.info(f"Received request to upload folder: {request.folder_path}")
    if not os.path.isdir(request.folder_path):
        logger.error(f"Folder not found: {request.folder_path}")
        raise HTTPException(status_code=404, detail="Folder not found")

    try:
        service = get_data_ingestion_service()
        result = service.upload_folder(request.folder_path)
        logger.info(f"Successfully processed folder: {request.folder_path}")
        return {
            "status": "success",
            "message": f"Folder {request.folder_path} processed",
            "result": result,
        }

    except Exception as e:
        logger.error(f"Error uploading folder {request.folder_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
