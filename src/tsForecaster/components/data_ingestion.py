import os
import opendatasets as od
from tsForecaster.entity.config_entity import DataIngestionConfig
from tsForecaster import logger

class DataIngestion:
    def __init__(self, config:DataIngestionConfig) -> None:
        self.config = config
    
    def download_file(self) ->None:
        try:
            download_dir = self.config.data_dir
            dataset_url = self.config.source_url
            os.makedirs(download_dir, exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {download_dir}")
            od.download(dataset_url, data_dir=download_dir)
            logger.info(f"Downloaded data from {dataset_url} into file {download_dir}")
        except Exception as e:
            raise e