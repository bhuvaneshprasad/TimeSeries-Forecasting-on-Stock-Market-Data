import os
from tsForecaster import logger
from tsForecaster.components.model_evaluation import ModelEvaluation
from tsForecaster.config.configuration import ConfigurationManager

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationPipeline:
    def __init__(self) -> None:

        pass
    
    def main(self, X, y, dates):
        try:
            config = ConfigurationManager()
            eval_config = config.get_model_training_config()
            eval = ModelEvaluation(eval_config)
            eval.evaluation(X, y, dates)
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e