import os
import opendatasets as od
import yfinance as yf
import pandas as pd
from tsForecaster.entity.config_entity import DataIngestionConfig
from tsForecaster import logger

class DataIngestion:
    def __init__(self, config:DataIngestionConfig) -> None:
        self.config = config
    
    def download_file(self) ->None:
        try:
            download_dir = self.config.data_dir
            dataset_url = self.config.source_url
            os.makedirs(download_dir, exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {download_dir}")
            od.download(dataset_url, data_dir=download_dir)
            logger.info(f"Downloaded data from {dataset_url} into file {download_dir}")
        except Exception as e:
            raise e
    
    def update_file(self) ->None:
        try:
            download_dir = self.config.data_dir
            ticker = yf.Ticker("^NSEI")
            history = ticker.history(start='2024-07-08', interval='1d')
            history.drop(columns=['Volume', 'Dividends', 'Stock Splits'], inplace=True)
            history = round(history, 2)
            history['Index Name'] = "NIFTY 50"
            history.reset_index(inplace=True)
            history['Date'] = history['Date'].dt.strftime('%d %b %Y')
            history = history[['Index Name', 'Date', 'Open', 'High', 'Low', 'Close']]
            history = history.sort_values(by=['Date'], ascending=False)
            df = pd.read_csv(os.path.join(download_dir ,"NIFTY 50_Historical.csv"))
            df = pd.concat([history, df], ignore_index=True)
            df = df[['Index Name', 'Date', 'Open', 'High', 'Low', 'Close']]
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.drop_duplicates(subset=['Date'])
            df.to_csv(os.path.join(download_dir ,"NIFTY 50_Historical.csv"))
        
        except Exception as e:
            raise e
    