import os
from pathlib import Path
from tsForecaster.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from tsForecaster.utils.common import read_yaml, create_directories
from tsForecaster.entity.config_entity import DataIngestionConfig, ModelTrainingConfig

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
            data_dir=config.data_dir,
            scaler_path=config.scaler_path
        )
        
        return data_ingestion_config
    
    def get_model_training_config(self) -> ModelTrainingConfig:
        model_training = self.config.model_training
        params = self.params
        
        create_directories([model_training.root_dir])
        
        model_training_config = ModelTrainingConfig(
            root_dir=Path(model_training.root_dir),
            training_model_path=Path(model_training.trained_model_path),
            training_data_path=Path(self.config.data_ingestion.data_dir),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_learning_rate=params.LEARNING_RATE,
            params_time_steps=params.TIME_STEPS
        )
        
        return model_training_config