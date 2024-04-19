import os
import pandas as pd
import subprocess
from line_profiler import LineProfiler

def clean_data():

    if not os.path.exists("/content/history.csv"):
        script_path = '/content/RawCode/data_scraping.py'
        subprocess.run(["python", script_path])

    hist = pd.read_csv("/content/history.csv")
    hist.dropna(inplace=True)
    hist.set_index("Date", inplace=True)

    stock_tickers = pd.read_excel("/content/stock_tickers.xlsx")
    tickers = stock_tickers["Stock_Ticker"].to_list()

    common_dates = None
    valid_tickers = []

    for ticker in tickers:
        stock_data = hist[hist['Ticker'] == ticker]
        
        if len(stock_data) < 8000:
          continue

        if common_dates is None:
          common_dates = set(stock_data.index.to_list())
        
        else:
          common_dates = common_dates.intersection(set(stock_data.index.to_list()))

        valid_tickers.append(ticker)

    hist = hist[hist['Ticker'].isin(valid_tickers)]
    cleaned_data = hist.loc[list(common_dates)]
    cleaned_data.to_csv("/content/cleaned_data.csv", index=True)

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler.add_function(clean_data)
    profiler.run("clean_data()")
    profiler.print_stats()
