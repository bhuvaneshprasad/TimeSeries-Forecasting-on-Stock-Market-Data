# TimeSeries-Forecasting-on-Stock-Market-Data

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-v3.12.2-v?label=Python&color=blue" alt="Python" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Tensorflow-v2.16.2-v?color=orange" alt="TensorFlow" /></a>
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-v0.111.0-v?color=%23009485" alt="FastAPI" /></a>
  <a href="https://github.com/bhuvaneshprasad/TimeSeries-Forecasting-on-Stock-Market-Data"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" /></a>
</p>

This project harnesses the capabilities of deep learning to predict time series data using Gated Recurrent Units (GRUs). By implementing a tailored GRU architecture in TensorFlow, the model demonstrated impressive performance, achieving high accuracy in forecasting future values. This AI-driven approach not only enhances the precision of time series predictions but also opens new avenues for research in various fields, from finance to environmental monitoring, fostering innovation in predictive analytics.

## Demo
**Note:** The project is deployed to huggingface spaces for demo purpose. The huggingface spaces may be down if not used, and it might take a couple of minutes to startup initially.

- You can click [here](https://huggingface.co/spaces/bhuvaneshprasad/timeseries-forecasting) to check the live demo of the streamlit app.

- Screenshots of the streamlit app are provided below.

<div align="center">
  <img src="assets/tsHome.png">
</div>

- Once the app is loaded click on the forcast button.

<div align="center">
  <img src="assets/tsForecast.png">
</div>

- The forecast for next 15 days will be displayed in a line chart and a table.

<div align="center">
  <img src="assets/tsResults.png">
</div>

## Lessons Learned

- **Importance of Data Preprocessing:** Properly preparing the dataset, including normalization and handling missing values, was crucial for improving model performance and ensuring accurate predictions.

- **Hyperparameter Tuning**: Experimenting with different hyperparameters (e.g., learning rate, batch size, number of layers) significantly impacted the model's accuracy and convergence speed, highlighting the need for thorough experimentation.

- **Cross-Validation for Consistency:** Implementing cross-validation was essential for assessing the model's performance across different datasets, ensuring reliability and robustness in predictions.

- **Model Evaluation and Visualization:** Visualizing predictions versus actual values, as well as analyzing residuals, provided valuable insights into model performance and areas for improvement, reinforcing the importance of thorough evaluation.

## Model Prediction

<div align="center">
  <img src="assets/model_prediction.png">
</div>

## Model Inference

- The model achieved a high training R² value of 94%, demonstrating its effectiveness in capturing the variance in the training data.

- With a strong validation R² of 88%, the model showed robust performance, indicating good generalization to unseen data and effective learning of underlying patterns.

- The model maintained a solid R² of 88% in testing, further validating its reliability and consistency across different datasets in predicting future values.

<div align="center">
  <img src="assets/test_data_forecast.png">
</div>

-  Analyzing the residual plot revealed specific areas of prediction error, providing insights into potential adjustments needed for future model improvements.

<div align="center">
  <img src="assets/residual_plot.png">
</div>

## Setup/Installation

To set up the project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/bhuvaneshprasad/TimeSeries-Forecasting-on-Stock-Market-Data
cd TimeSeries-Forecasting-on-Stock-Market-Data
```

### 2. Install Dependencies
- Create a virtual environment (recommended) and install the required packages:

```bash
python -m venv venv
venv\Scripts\activate  # On Linux use `source venv/bin/activate`
pip install -r requirements.txt
```

### 3. Run the Project

- To get the model artifacts like datasets, scaler and model train the model using below command

```bash
python main.py
```

- After getting the artifacts, run streamlit app using below command

```bash
python streamlit/app.py
```

- To test the API route use below command

```bash
uvicorn app:app --reload
```

- The API endpoint will be available at https://localhost:8000/forecast

**Note:** 
1. You can adjust the parameters in params.yaml to experiment with different configurations.

2. If you get any error check streamlit/app.py and app.py in the root directories for the correct file paths of the artifacts.

## Acknowledgements

- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)

## Authors

- [Bhuvanesh Prasad](https://www.github.com/bhuvaneshprasad)


## License

- [MIT License](https://github.com/bhuvaneshprasad/TimeSeries-Forecasting-on-Stock-Market-Data/blob/main/LICENSE)
