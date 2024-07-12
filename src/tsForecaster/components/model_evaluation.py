from pathlib import Path
from matplotlib import pyplot as plt
import tensorflow as tf
from tsForecaster.entity.config_entity import ModelTrainingConfig
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class ModelEvaluation:
    def __init__(self, config:ModelTrainingConfig) -> None:
        self.config = config
    
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def evaluation(self, X, y, dates):
        self.model = self.load_model(self.config.training_model_path)
        y_pred = self.model.predict(X).flatten()
        
        plt.figure(figsize=(15, 5))
        plt.plot(dates, y)
        plt.plot(dates, y_pred)
        plt.legend(['y-true', 'y-pred'])
        plt.show()
        
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        rmse = mean_squared_error(y, y_pred, squared=False)
        r2 = r2_score(y, y_pred)
        
        return mae, mse, rmse, r2