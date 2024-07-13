import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tsForecaster.entity.config_entity import DataIngestionConfig
from tsForecaster import logger

class DataPreProcessing:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config

    def process_csv(self) -> pd.DataFrame:
        logger.info("Processing data from CSV to DataFrame")
        df_path = Path(self.config.data_dir) / "NIFTY 50_Historical.csv"
        df = pd.read_csv(df_path, index_col=[0])
        df.drop(columns=['Index Name', 'Open', 'High', 'Low'], inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        
        start_date = '1990-07-03'
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        date_df = pd.DataFrame(date_range, columns=['Date'])
        df = pd.merge(date_df, df, how='left', on='Date')
        df = df.ffill()
        
        df['Close%'] = ((df['Close'] / df['Close'].shift(1)) - 1) * 100
        for period, days in {
            '1D': 1, '2D': 2, '3D': 3, '1W': 7, '2W': 14, '1M': 30, '2M': 60,
            '3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095, '5Y': 1825,
            '7Y': 2555, '10Y': 3650
        }.items():
            df[f'Close_{period}_ago'] = df['Close%'].shift(days)
            
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.set_index('Date', inplace=True)
        
        logger.info("Done processing data from CSV to DataFrame")
        return df

    def scaling_data(self, df: pd.DataFrame):
        logger.info("Scaling data...")
        scaler = MinMaxScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
        joblib.dump(scaler, Path(os.path.join(self.config.scaler_path, 'scaler.pkl')))
        logger.info("Data scaling done")
        return df_scaled
    
    def create_sequences(self, df: pd.DataFrame, time_steps: int):
        logger.info("Creating X, y sequences...")
        X, y = [], []
        for i in range(len(df) - time_steps):
            X.append(df.iloc[i: i + time_steps, 1:].values)
            y.append(df.iloc[i, 0])
        dates = df.index[time_steps:]
        logger.info("X, y sequences created")
        return np.array(X), np.array(y), dates

    def train_test_split(self, X, y, dates, train_len=0.8, val_len=0.1, test_len=0.1):
        logger.info("Splitting train, val, test data...")
        total_len = train_len + val_len + test_len
        if total_len != 1.0:
            logger.error("Error splitting train, val, test data: Total length is not equal to 1")
            raise ValueError("Aggregate length of train, validation, and test lengths should be equal to 1")
        
        total_size = len(y)
        train_size = int(total_size * train_len)
        val_size = int(total_size * val_len)
        
        X_train, X_val, X_test = X[:train_size], X[train_size:train_size+val_size], X[train_size+val_size:]
        y_train, y_val, y_test = y[:train_size], y[train_size:train_size+val_size], y[train_size+val_size:]
        dates_train, dates_val, dates_test = dates[:train_size], dates[train_size:train_size+val_size], dates[train_size+val_size:]
        
        logger.info("Done splitting train, val, test data")
        return X_train, X_val, X_test, y_train, y_val, y_test, dates_train, dates_val, dates_test