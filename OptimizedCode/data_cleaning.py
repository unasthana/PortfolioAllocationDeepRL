import os
import subprocess
import pandas as pd
import multiprocessing as mp
from line_profiler import LineProfiler

def process_chunk(tickers_chunk, hist):
    filtered_data = hist[hist['Ticker'].isin(tickers_chunk)]

    ticker_counts = filtered_data['Ticker'].value_counts()
    valid_tickers = ticker_counts.index[ticker_counts >= 8000]
    filtered_data = filtered_data[filtered_data['Ticker'].isin(valid_tickers)].copy()

    filtered_data.reset_index(inplace=True)
    grouped_dates = filtered_data.groupby('Ticker')['Date'].agg(set)
    common_dates_chunk = set.intersection(*grouped_dates)

    return common_dates_chunk

def parallel_process(tickers, hist, chunk_size):
    num_processes = mp.cpu_count()
    tickers_chunks = [tickers[i:i+chunk_size] for i in range(0, len(tickers), chunk_size)]
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.starmap(process_chunk, [(chunk, hist) for chunk in tickers_chunks])
    
    common_dates = set.intersection(*results)
    
    return common_dates

def clean_data():
    if not os.path.exists("/content/history.csv"):
        script_path = '/content/OptimizedCode/data_scraping.py'
        subprocess.run(["python", script_path])

    hist = pd.read_csv("/content/history.csv")
    hist.dropna(inplace=True)
    hist.set_index("Date", inplace=True)
    
    stock_tickers = pd.read_excel("/content/stock_tickers.xlsx")
    tickers = stock_tickers["Stock_Ticker"].to_list()

    chunk_size = (len(tickers) // mp.cpu_count()) + 1
    common_dates = parallel_process(tickers, hist, chunk_size)
    
    cleaned_data = hist.loc[list(common_dates)]
    cleaned_data.to_csv("/content/cleaned_data.csv", index=True)

if __name__ == "__main__":
    profiler = LineProfiler()
    profiler.add_function(clean_data)
    profiler.run("clean_data()")
    profiler.print_stats()
