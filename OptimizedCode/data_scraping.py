import os
import yfinance as yf
import pandas as pd
from line_profiler import LineProfiler

def download_data():
    stock_tickers = pd.read_excel("/content/stock_tickers.xlsx")
    tickers = stock_tickers["Stock_Ticker"].to_list()
    hist = yf.download(tickers=tickers, period="max", interval='1d')

    dataset = pd.concat([hist.xs(key=ticker, level=1, axis=1).assign(Ticker=ticker) for ticker in tickers])
    dataset.to_csv("/content/history.csv", index=True)

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler.add_function(download_data)
    profiler.run("download_data()")
    profiler.print_stats()
