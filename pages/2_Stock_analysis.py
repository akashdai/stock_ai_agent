import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "stock prices.csv")

st.title("📊 Stock Analysis")

symbols = sorted(df["symbol"].unique())

symbol = st.selectbox(
    "Select Stock",
    symbols
)

if st.button("Analyze"):

    stock = df[df["symbol"] == symbol.upper()]

    if stock.empty:

        st.error("Stock not found")

    else:

        stock = stock.sort_values("date")

        stock["MA50"] = stock["close"].rolling(50).mean()
        stock["MA200"] = stock["close"].rolling(200).mean()

        latest = stock["close"].iloc[-1]
        avg50 = stock["close"].tail(50).mean()

        if latest > avg50:
            st.success("📈 Uptrend Detected")
        else:
            st.warning("📉 Downtrend Detected")

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"${stock['close'].iloc[-1]:.2f}"
        )

        col2.metric(
            "Highest Price",
            f"${stock['close'].max():.2f}"
        )

        col3.metric(
            "Average Volume",
            f"{stock['volume'].mean():,.0f}"
        )

        st.subheader("Dataset Information")
        st.write(f"Total Records: {len(stock)}")

        st.subheader("Summary Statistics")
        st.dataframe(stock.describe())

        st.subheader("Latest Stock Data")
        st.dataframe(stock.tail())

        st.subheader("📈 Stock Trend")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=stock["date"],
                y=stock["close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=stock["date"],
                y=stock["MA50"],
                mode="lines",
                name="50 Day MA"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=stock["date"],
                y=stock["MA200"],
                mode="lines",
                name="200 Day MA"
            )
        )

        fig.update_layout(
            template="plotly_dark",
            title=f"{symbol} Stock Analysis",
            xaxis_title="Date",
            yaxis_title="Price",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🕯️ Candlestick Chart")

        candle = go.Figure(
            data=[
                go.Candlestick(
                    x=stock["date"],
                    open=stock["open"],
                    high=stock["high"],
                    low=stock["low"],
                    close=stock["close"]
                )
            ]
        )

        candle.update_layout(
            template="plotly_dark",
            title=f"{symbol} Candlestick Chart",
            height=700
        )

        st.plotly_chart(candle, use_container_width=True)

        

        st.subheader("Key Insights")

        st.write(f"Highest Close Price: {stock['close'].max():.2f}")
        st.write(f"Lowest Close Price: {stock['close'].min():.2f}")
        st.write(f"Average Close Price: {stock['close'].mean():.2f}")
        st.write(f"Average Volume: {stock['volume'].mean():,.0f}")


















































