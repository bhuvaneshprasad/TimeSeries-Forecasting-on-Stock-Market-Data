from tsForecaster.components.data_preprocessing import DataPreProcessing
from tsForecaster import logger
from tsForecaster.config.configuration import ConfigurationManager

STAGE_NAME = "Data Pre-Processing Stage"

class DataPreProcessingPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_preprocessing = DataPreProcessing(config=data_ingestion_config)
            df = data_preprocessing.process_csv()
            close_df = df['Close']
            df.drop(columns=['Close'], inplace=True)
            scaled_df = data_preprocessing.scaling_data(df)
            time_steps = 60
            X, y, dates = data_preprocessing.create_sequences(scaled_df, time_steps)
            X_train, X_val, X_test, y_train, y_val, y_test, dates_train, dates_val, dates_test = data_preprocessing.train_test_split(X, y, dates, train_len=0.8, val_len=0.1, test_len=0.1)
            
            return X_train, X_val, X_test, y_train, y_val, y_test, dates_train, dates_val, dates_test, close_df
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataPreProcessingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e