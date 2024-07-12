import os
import joblib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from tsForecaster.components.data_preprocessing import DataPreProcessing
from tsForecaster.config.configuration import ConfigurationManager
from tsForecaster.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from tsForecaster.pipeline.stage_02_data_preprocessing import DataPreProcessingPipeline
from tsForecaster.utils.common import create_directories, read_yaml

def create_features(df, pred):
    
    df = df['Close%']
    new_date = pd.date_range(df.index[-1] + pd.DateOffset(days=1), periods=1, freq='D')
    new_close_value = pred
    
    new_row = pd.DataFrame({'Close%': new_close_value}, index=[pd.to_datetime(new_date.values[0])])
    df = pd.concat([df, new_row])
    
    df['Close_1D_ago'] = df['Close%'].shift(1)
    df['Close_2D_ago'] = df['Close%'].shift(2)
    df['Close_3D_ago'] = df['Close%'].shift(3)
    df['Close_1W_ago'] = df['Close%'].shift(7)
    df['Close_2W_ago'] = df['Close%'].shift(14)
    df['Close_1M_ago'] = df['Close%'].shift(30)
    df['Close_2M_ago'] = df['Close%'].shift(60)
    df['Close_3M_ago'] = df['Close%'].shift(90)
    df['Close_6M_ago'] = df['Close%'].shift(180)
    df['Close_1Y_ago'] = df['Close%'].shift(365)
    df['Close_2Y_ago'] = df['Close%'].shift(930)
    df['Close_3Y_ago'] = df['Close%'].shift(1095)
    df['Close_5Y_ago'] = df['Close%'].shift(1825)
    df['Close_7Y_ago'] = df['Close%'].shift(2555)
    df['Close_10Y_ago'] = df['Close%'].shift(3650)
    
    return df

def forecast(model, df, X, time_steps, scaler, close_df, future_steps=15, fig=False) -> pd.DataFrame:
    future_predictions = []
    last_row = X[-1:]
    df_forecast = df.copy()

    for step in range(future_steps):
        
        next_close = model.predict(last_row)
        future_predictions.append(next_close[0, 0])
        df_forecast = create_features(df_forecast, next_close[0, 0])
        last_row = df_forecast.iloc[-60:, 1:].values.reshape(1, time_steps, 15)

    predicted_prices = np.array(future_predictions).reshape(-1, 1)
    predicted_full_features = np.concatenate((predicted_prices, np.zeros((future_steps, 15))), axis=1)
    predicted_values = scaler.inverse_transform(predicted_full_features)[:, 0]
    predicted_values_list = predicted_values.flatten().tolist()

    last_close = close_df.values[-1]

    future_closes = []

    for i in range(predicted_values_list.__len__()):
        next_close = last_close * (1 + (predicted_values_list[i] / 100))
        future_closes.append(next_close)
        next_close = last_close

    # Create a DataFrame for future predictions
    future_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(1), periods=future_steps, freq='D')
    future_df = pd.DataFrame(future_closes, index=future_dates, columns=['Close'])

    if fig:
        plt.figure(figsize=(15, 5))
        plt.plot(future_dates, future_df)
        plt.show()
    
    return future_df

def main() -> pd.DataFrame:
    config_file = read_yaml(CONFIG_FILE_PATH)
    params = read_yaml(PARAMS_FILE_PATH)
    
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_preprocessing = DataPreProcessing(config=data_ingestion_config)
    
    df = data_preprocessing.process_csv()
    close_df = df['Close']
    df.drop(columns=['Close'], inplace=True)

    scaled_df = data_preprocessing.scaling_data(df)
    scaler = joblib.load(os.path.join(config_file.data_ingestion.scaler_path, 'scaler.pkl'))
    
    X, y, dates = data_preprocessing.create_sequences(scaled_df, params.TIME_STEPS)
    model = tf.keras.models.load_model(config_file.model_training.trained_model_path)
    
    forecast_df = forecast(model, scaled_df, X, params.TIME_STEPS, scaler, close_df, future_steps=15)
    
    return forecast_df

if __name__ == '__main__':
    forecast = main()
    print(forecast)
