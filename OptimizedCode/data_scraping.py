import os
import yfinance as yf
import pandas as pd
from line_profiler import LineProfiler

def scrape_data():
    stock_tickers = pd.read_excel("/content/stock_tickers.xlsx")
    tickers = stock_tickers["Stock_Ticker"].to_list()
    hist = yf.download(tickers=tickers, period="max", interval='1d')

    dataset = pd.concat([hist.xs(key=ticker, level=1, axis=1).assign(Ticker=ticker) for ticker in tickers])

    return dataset

def run_scrape_data():
    profiler = LineProfiler()
    profiler.add_function(scrape_data)

    profiler.enable_by_count()
    history = scrape_data()
    profiler.disable_by_count()

    profiler.print_stats()

    return history
