import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objs as go

root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))

import forecaster

def main():
    st.set_page_config(page_title="Nifty 50 Forecast")
    st.title("Time Series Forecasting - Nifty 50")
    
    if st.button("Forecast"):
        with st.spinner('Forecasting...'):
            forecast_df = forecaster.main()
            forecast_df = forecast_df.round(2)
            st.write(forecast_df)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df["Close"], mode='lines+markers', name='Forecasted Values'))
            
            fig.update_layout(
                title='Nifty 50 Close Forecast',
                xaxis_title='Date',
                yaxis_title='Close (Forecasted)',
                xaxis_tickangle=-90,
                width=800,
                height=600
            )
            
            st.plotly_chart(fig)
            

if __name__ == "__main__":
    main()
