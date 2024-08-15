# %%
import sys
import os

sys.path.append('/Users/raphaelravinet/Code')
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime, timedelta
import logging
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import ta
from algo_trading.log_config import setup_logging
from Fin_Database.Data.connect import engine, DailyStockData, HourlyStockData, OneMinuteStockData, FiveMinuteStockData,FifteenMinuteStockData, StockSplits, StockNews, CompanyFinancials
from algo_trading.Pre_Processing.pre_processing import PreProcessing

# %%
aapl_min = pd.read_parquet('/Users/raphaelravinet/Code/algo_trading/Datasets/Minute_Data/aapl_minute.parquet')
msft_min = pd.read_parquet('/Users/raphaelravinet/Code/algo_trading/Datasets/Minute_Data/msft_minute.parquet')
aapl_daily = pd.read_csv('/Users/raphaelravinet/Code/algo_trading/Datasets/Daily_Data/aapl_daily.csv')
msft_daily = pd.read_csv('/Users/raphaelravinet/Code/algo_trading/Datasets/Daily_Data/msft_daily.csv')


# %%
aapl_hourly = pd.read_parquet('/Users/raphaelravinet/Code/algo_trading/Datasets/Hourly_Data/aapl_hourly.parquet')
msft_hourly = pd.read_parquet('/Users/raphaelravinet/Code/algo_trading/Datasets/Hourly_Data/msft_hourly.parquet')

# %%
aapl_daily = PreProcessing(aapl_daily).setting_index().df
msft_daily = PreProcessing(msft_daily).setting_index().df
aapl_min = PreProcessing(aapl_min).filter_market_hours().setting_index().df
msft_min = PreProcessing(msft_min).filter_market_hours().setting_index().df
aapl_hourly = PreProcessing(aapl_hourly).filter_market_hours().setting_index().df
msft_hourly = PreProcessing(msft_hourly).filter_market_hours().setting_index().df



# %%
fast_periods = [5, 10, 30]
slow_periods = [50, 100, 200,300]
periods = fast_periods + slow_periods

# %%
class TechnicalIndicators:
    def __init__(self, df):
        self.df = df
        
    def calculate_log_return(self):
        self.df['log_ret'] = np.log(self.df['close']) - np.log(self.df['close'].shift(1))[1:]
        return self.df

    def calculate_rsi(self, window=14):
        self.df[f'RSI_{window}'] = ta.momentum.RSIIndicator(self.df['close'], window=window).rsi()
        return self

    def calculate_macd(self):
        self.df['MACD'] = ta.trend.MACD(self.df['close']).macd_diff()
        return self

    def calculate_roc(self, window=14):
        self.df['ROC'] = ta.momentum.roc(self.df['close'], window=window)
        return self

    def calculate_stoch(self, window=14):
        self.df['Stoch'] = ta.momentum.stoch(self.df['high'], self.df['low'], self.df['close'], window=window)
        return self

    def calculate_adx(self, window=14):
        self.df['ADX'] = ta.trend.ADXIndicator(self.df['high'], self.df['low'], self.df['close'], window=window).adx()
        self.df['ADX_pos'] = ta.trend.ADXIndicator(self.df['high'], self.df['low'], self.df['close'], window=window).adx_pos()
        self.df['ADX_neg'] = ta.trend.ADXIndicator(self.df['high'], self.df['low'], self.df['close'], window=window).adx_neg()
        return self

    def calculate_hl_mean(self, window=25):
        self.df[f'rolling_H-L_{window}'] = (self.df['high'] - self.df['low']).rolling(window=window).mean()
        return self
    
    def calculate_lower_band(self, window = 10):
        self.df['lower_band'] = self.df['high'].rolling(window=10).max() - 2.5 * self.df['rolling_H-L_25']
        return self
    
    def calculate_atr(self, window=14):
        self.df['ATR'] = ta.volatility.AverageTrueRange(self.df['high'], self.df['low'], self.df['close'], window=window).average_true_range()
        return self

    def calculate_ibs(self):
        self.df['IBS'] = (self.df['close'] - self.df['low']) / (self.df['high'] - self.df['low'])
        return self

    def calculate_obv(self):
        self.df['OBV'] = ta.volume.OnBalanceVolumeIndicator(self.df['close'], self.df['volume']).on_balance_volume()
        return self
    
    
    def calculate_moving_averages(self, periods):
        for period in periods:
            self.df[f'sma_{period}'] = ta.trend.sma_indicator(self.df['close'], window=period)
            self.df[f'ema_{period}'] = ta.trend.ema_indicator(self.df['close'], window=period)
        return self
    
    def calculate_slope(self, series, n):
        def series_slope(y):
            x = np.arange(len(y))
            slope, _ = np.polyfit(x, y, 1)
            pct_slope = (slope / y[0]) * 100
            return pct_slope
        
        slopes = series.rolling(window=n).apply(series_slope, raw=True)
        return slopes
    
    def calculate_moving_average_slopes(self, periods, slope_period):
        """Calculate the slope of both SMA and EMA for each period in periods"""
        for period in periods:
            self.df[f'sma_slope_{period}'] = self.calculate_slope(self.df[f'sma_{period}'], slope_period)
            self.df[f'ema_slope_{period}'] = self.calculate_slope(self.df[f'ema_{period}'], slope_period)
        return self

    def add_technical_indicators(self, periods, slope_period = 5):
        self.calculate_rsi()
        self.calculate_rsi(window=2)
        self.calculate_macd()
        self.calculate_log_return()
        self.calculate_roc()
        self.calculate_stoch()
        self.calculate_adx()
        self.calculate_hl_mean()
        self.calculate_atr()
        self.calculate_ibs()
        self.calculate_obv()
        self.calculate_moving_averages(periods)
        # self.calculate_moving_average_slopes(periods, slope_period)
        return self.df

# %%
class features:
    def __init__(self, df):
        self.df = df
    
    def date_features(self):
        self.df['day'] = self.df['date'].dt.day
        self.df['month'] = self.df['date'].dt.month
        self.df['day_of_week'] = self.df['date'].dt.dayofweek
        return self.df
    #add date/time to next corporate announcement
    
    


