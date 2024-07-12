import tensorflow as tf
from pathlib import Path
from tsForecaster.entity.config_entity import ModelTrainingConfig
from tsForecaster.utils.common import create_directories


class ModelTraining:
    def __init__(self, config: ModelTrainingConfig) -> None:
        self.config = config
        self.model = self.create_model()
        
        create_directories([config.root_dir])
    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
    
    def create_model(self) -> tf.keras.Model:
        model = tf.keras.models.Sequential([
                    tf.keras.layers.Input((self.config.params_time_steps, 15)),
                    tf.keras.layers.GRU(128, return_sequences=True),
                    tf.keras.layers.GRU(128, return_sequences=False),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(1)
                    ])
        
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.params_learning_rate), metrics=['mean_squared_error'])
        
        model.summary()
        
        return model
    
    def train(self, X_train, y_train, X_val, y_val):
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
        history = self.model.fit(
                        X_train,
                        y_train,
                        validation_data=(X_val, y_val),
                        epochs=self.config.params_epochs,
                        batch_size=self.config.params_batch_size,
                        callbacks=[early_stop]
                    )
        self.save_model(path=self.config.training_model_path, model=self.model)
        return history