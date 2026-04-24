import os
from loguru import logger
from pageindex import PageIndexClient


def submit_folder_to_pi(pi_client: PageIndexClient, folder_path: str):
    try:
        if not os.path.isdir(folder_path):
            raise ValueError(f"Invalid folder path: {folder_path}")

        responses = []

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".pdf"):
                file_path = os.path.join(folder_path, file_name)

                res = pi_client.submit_document(file_path)

                if res:
                    responses.append(res)

        logger.info(f"Uploaded {len(responses)} files from folder.")

        return responses

    except Exception:
        logger.exception("Failed to upload folder")
        return []
