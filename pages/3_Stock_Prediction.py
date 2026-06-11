import streamlit as st
import pandas as pd
from pathlib import Path
from prophet import Prophet
import plotly.graph_objects as go

# Load Dataset
BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "stock prices.csv")

# Page Title
st.title("📈 Stock Prediction")

# Stock Selector
symbols = sorted(df["symbol"].unique())

symbol = st.selectbox(
    "Select Stock",
    symbols
)

# Predict Button
if st.button("Predict"):

    stock = df[df["symbol"] == symbol.upper()]

    if stock.empty:

        st.error("Stock not found")

    else:

        stock = stock.sort_values("date")

        # Prophet Format
        prophet_df = stock[["date", "close"]].copy()

        prophet_df.columns = ["ds", "y"]

        prophet_df["ds"] = pd.to_datetime(
            prophet_df["ds"]
        )

        # Train Model
        model = Prophet()

        model.fit(prophet_df)

        # Future Dates
        future = model.make_future_dataframe(
            periods=30
        )

        forecast = model.predict(future)

        # Prediction Table
        st.subheader("📅 Predicted Next 30 Days")

        st.dataframe(
            forecast[
                ["ds", "yhat", "yhat_lower", "yhat_upper"]
            ].tail(30)
        )

        # Forecast Chart
        st.subheader("📈 Forecast Chart")

        forecast_plot = go.Figure()

        # Forecast Line
        forecast_plot.add_trace(
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat"],
                mode="lines",
                name="Forecast"
            )
        )

        # Upper Bound
        forecast_plot.add_trace(
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_upper"],
                mode="lines",
                name="Upper Bound"
            )
        )

        # Lower Bound
        forecast_plot.add_trace(
            go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_lower"],
                mode="lines",
                name="Lower Bound"
            )
        )

        forecast_plot.update_layout(
            template="plotly_dark",
            title=f"{symbol} 30-Day Forecast",
            xaxis_title="Date",
            yaxis_title="Predicted Price",
            height=600
        )

        st.plotly_chart(
            forecast_plot,
            use_container_width=True
        )

        # Trend Analysis
        st.subheader("📊 Trend Analysis")

        trend_fig = go.Figure()

        trend_fig.add_trace(
            go.Scatter(
                x=forecast["ds"],
                y=forecast["trend"],
                mode="lines",
                name="Trend"
            )
        )

        trend_fig.update_layout(
            template="plotly_dark",
            title="Trend Component",
            xaxis_title="Date",
            yaxis_title="Trend Value",
            height=500
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

        # Summary Metrics
        current_price = stock["close"].iloc[-1]

        predicted_price = forecast["yhat"].iloc[-1]

        change_pct = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        st.subheader("📋 Prediction Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"${current_price:.2f}"
        )

        col2.metric(
            "Predicted Price",
            f"${predicted_price:.2f}"
        )

        col3.metric(
            "Expected Change",
            f"{change_pct:.2f}%"
        )

        if change_pct > 0:
            st.success(
                "📈 Model suggests a positive trend over the next 30 days."
            )
        else:
            st.warning(
                "📉 Model suggests a negative trend over the next 30 days."
            )