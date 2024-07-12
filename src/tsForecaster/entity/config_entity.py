from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: Path
    data_dir: Path
    scaler_path: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    training_model_path: Path
    training_data_path: Path
    params_time_steps: int
    params_epochs: int
    params_batch_size: int
    params_learning_rate: float
    