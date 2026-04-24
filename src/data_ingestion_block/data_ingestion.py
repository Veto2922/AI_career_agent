import os
from typing import List, Optional
from dotenv import load_dotenv
from loguru import logger
from pageindex import PageIndexClient

from src.data_ingestion_block.utils.submit_file import submit_file_to_pi
from src.data_ingestion_block.utils.submit_folder import submit_folder_to_pi


class DataIngestion:
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()

        self.api_key = api_key or os.getenv("Page_index_api")

        if not self.api_key:
            raise ValueError("PageIndex API key is missing.")

        self.pi_client = PageIndexClient(api_key=self.api_key)

    # Upload Single File
    def upload_file(self, file_path: str) -> dict:
        submit_file_to_pi(self.pi_client, file_path)

    # Upload Folder
    def upload_folder(self, folder_path: str) -> List[dict]:
        submit_folder_to_pi(self.pi_client, folder_path)
