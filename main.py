# from dotenv import load_dotenv
from tsForecaster import logger
from tsForecaster.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from tsForecaster.pipeline.stage_02_data_preprocessing import DataPreProcessingPipeline
from tsForecaster.pipeline.stage_03_model_training import ModelTrainingPipeline
from tsForecaster.pipeline.stage_04_model_evaluation import ModelEvaluationPipeline

# load_dotenv()

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Pre-Processing Stage"

try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = DataPreProcessingPipeline()
    X_train, X_val, X_test, y_train, y_val, y_test, dates_train, dates_val, dates_test, close_df = obj.main()
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Training"

try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = ModelTrainingPipeline()
    obj.main(X_train, y_train, X_val, y_val)
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Evaluation Stage"

try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
    obj = ModelEvaluationPipeline()
    obj.main(X_test, y_test, dates_test)
    logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
except Exception as e:
    logger.exception(e)
    raise e