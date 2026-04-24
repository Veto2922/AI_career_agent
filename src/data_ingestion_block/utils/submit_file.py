import os
from loguru import logger
from pageindex import PageIndexClient


def submit_file_to_pi(pi_client: PageIndexClient, file_path: str):
    try:
        if not os.path.isfile(file_path):
            raise ValueError(f"Invalid file path: {file_path}")
        if not file_path.endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")

        logger.info(f"Uploading file: {file_path}")

        response = pi_client.submit_document(file_path)
        logger.success(f"Uploaded successfully: {file_path}")
        return response

    except Exception:
        logger.exception(f"Failed to upload file: {file_path}")
        return {}
