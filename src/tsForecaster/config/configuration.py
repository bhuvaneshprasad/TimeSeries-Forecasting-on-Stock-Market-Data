import os
from tsForecaster.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from tsForecaster.utils.common import read_yaml, create_directories
from tsForecaster.entity.config_entity import DataIngestionConfig
from pathlib import Path

class ConfigurationManager:
    def __init__(self, config_file_path=CONFIG_FILE_PATH, params_file_path=PARAMS_FILE_PATH) -> None:
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        
        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            data_dir=config.data_dir
        )
        
        return data_ingestion_config