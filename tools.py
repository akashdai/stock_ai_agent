'''
import pandas as pd
import matplotlib.pyplot as plt


def load_stock_data():

    df = pd.read_csv("data/stock_prices.csv")

    return df


def get_summary():

    df = load_stock_data()

    return df.describe()


def plot_stock(symbol):

    df = load_stock_data()

    stock = df[df['Ticker'] == symbol]

    plt.figure(figsize=(10,5))
    plt.plot(stock['Date'], stock['Close'])

    plt.title(symbol)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("chart.png")

    return "chart.png"

import pandas as pd

DATA_PATH = "stock_prices.csv"   # adjust if needed

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def get_stock_data(symbol):

    df = load_data()

    stock = df[df["symbol"] == symbol.upper()]

    return stock

def stock_summary(symbol):

    stock = get_stock_data(symbol)

    return stock.describe()
    '''

import pandas as pd

DATA_PATH = "stock prices.csv"

def load_data():
    return pd.read_csv(DATA_PATH)

def stock_summary(symbol):

    df = load_data()

    stock = df[df["symbol"] == symbol]

    if stock.empty:
        return f"{symbol} not found in dataset"

    return stock.describe()




