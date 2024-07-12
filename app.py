from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import forecaster

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/forecast")
def forecast():
    try:
        forecast_df = forecaster.main()
        forecast_data = [
            {"date": date.strftime("%Y-%m-%d"), "value": value}
            for date, value in zip(forecast_df.index, forecast_df["Close"])
        ]
    except Exception as e:
        raise e

    return forecast_data

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)