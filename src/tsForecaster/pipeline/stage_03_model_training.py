from tsForecaster.components.model_training import ModelTraining
from tsForecaster.config.configuration import ConfigurationManager
from tsForecaster import logger

STAGE_NAME = "Model Training"

class ModelTrainingPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self, X_train, y_train, X_val, y_val):
        try:
            config = ConfigurationManager()
            model_training_config = config.get_model_training_config()
            model_training = ModelTraining(config=model_training_config)
            model_training.train(X_train, y_train, X_val, y_val)
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelTrainingPipeline()
        history = obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e