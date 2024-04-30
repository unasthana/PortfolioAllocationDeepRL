import pandas as pd
import numpy as np
from line_profiler import LineProfiler

def calculate_macd(df):
    df['EMA12'] = df['Close'].ewm(span=12, min_periods=12).mean()
    df['EMA26'] = df['Close'].ewm(span=26, min_periods=26).mean()

    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, min_periods=9).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal']

    return df

def calculate_bollinger_bands(df):
    df['RM20'] = df['Close'].rolling(window=20).mean()
    df['STD20'] = df['Close'].rolling(window=20).std()

    df['BB_Upper'] = df['RM20'] + (2 * df['STD20'])
    df['BB_Lower'] = df['RM20'] - (2 * df['STD20'])

    return df

def calculate_rsi(df):
    df['Delta'] = df['Close'].diff()
    
    df['Gain'] = df['Delta'].apply(lambda x: x if x > 0 else 0).rolling(window=14, min_periods=1).mean()
    df['Loss'] = -df['Delta'].apply(lambda x: x if x < 0 else 0).rolling(window=14, min_periods=1).mean()

    df['RS'] = df['Gain'] / (df['Loss'].replace(0, 0.0001)) 
    df['RSI'] = 100 - (100 / (1 + df['RS']))

    return df

def calculate_ADL(df):
    df['MFM'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low']).replace(0, np.inf)
    df['MFV'] = df['MFM'] * df['Volume']
    df['ADL'] = df['MFV'].cumsum()
   
    return df

def calculate_ichimoku_cloud(df):
    df['Tenkan Sen'] = (df['High'].rolling(window=9).max() + df['Low'].rolling(window=9).min()) / 2
    df['Kijun Sen'] = (df['High'].rolling(window=26).max() + df['Low'].rolling(window=26).min()) / 2
    df['Senkou Span A'] = ((df['Tenkan Sen'] + df['Kijun Sen']) / 2).shift(26)
    df['Senkou Span B'] = ((df['High'].rolling(window=52).max() + df['Low'].rolling(window=52).min()) / 2).shift(26)

    return df

def get_covariance_matrix(df):
    df.reset_index(inplace=True)
    df = df.sort_values(['Date','Ticker'],ignore_index=True)
    df.index = df.Date.factorize()[0]

    lookback = 252
    cov_list = []

    price_pivot = df.pivot_table(index='Date', columns='Ticker', values='Close')
    returns = price_pivot.pct_change().dropna()

    for i in range(lookback, len(returns)):
        returns_lookback = returns.iloc[i-lookback:i]
        covs = returns_lookback.cov().values
        cov_list.append(covs)

    cov_dates = returns.index[lookback:]
    df_cov = pd.DataFrame({'Date': cov_dates, 'Cov_List': cov_list})
    df = df.merge(df_cov, on='Date', how='right')

    df.sort_values(['Date', 'Ticker'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.set_index('Date', inplace=True)
    
    return df

def process_data(cleaned_data):  
    cleaned_data.reset_index(inplace=True) 
    cleaned_data.sort_values(by=['Ticker', 'Date'], inplace=True)
    cleaned_data.set_index("Date", inplace=True)

    df_group = cleaned_data.groupby('Ticker')

    macd_data = df_group.apply(calculate_macd)
    bb_data = df_group.apply(calculate_bollinger_bands) 
    rsi_data = df_group.apply(calculate_rsi)
    adl_data = df_group.apply(calculate_ADL)
    ichimoku_cloud_data = df_group.apply(calculate_ichimoku_cloud)

    feature_data = pd.concat([macd_data, bb_data[['BB_Lower', 'BB_Upper']], 
                               rsi_data['RSI'], adl_data['ADL'], 
                               ichimoku_cloud_data[['Tenkan Sen', 'Kijun Sen', 'Senkou Span A', 'Senkou Span B']]], axis=1)
    
    feature_data.drop(columns=['Ticker', 'EMA12', 'EMA26'], inplace=True)
    feature_data.reset_index(inplace=True)
    feature_data.set_index('Date', inplace=True)
    feature_data.dropna(inplace=True)
    
    preprocessed_data = get_covariance_matrix(feature_data)

    preprocessed_data.index = pd.to_datetime(preprocessed_data.index)
    preprocessed_data['Day'] = (preprocessed_data.index - preprocessed_data.index.min()).days

    return preprocessed_data

def run_preprocess_data(cleaned_data):
    profiler = LineProfiler()
    profiler.add_function(process_data)
    
    profiler.enable_by_count()
    preprocessed_data = process_data(cleaned_data)
    profiler.disable_by_count()

    profiler.print_stats()

    return preprocessed_data