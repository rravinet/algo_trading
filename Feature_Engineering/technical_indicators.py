# %%
import sys
import os

sys.path.append(os.getenv("CODE_PATH"))
sys.path.append(os.getenv("FIN_DATABASE_PATH"))

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
class TechnicalIndicators:
    def __init__(self, df):
        self.df = df
        
    def calculate_log_return(self, lags):
        for lag in lags:
            self.df[f'log_ret_{lag}'] = np.log(self.df['close']) - np.log(self.df['close'].shift(lag))
        return self
   
    def calculate_return(self):
        self.df['return'] = self.df['close'].pct_change()
        return self

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
    
    def calculate_open_close_diff(self):
        self.df['o_close_diff'] = self.df['open'] - self.df['close'].shift(1)
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
    
    def calculate_moving_average_slopes(self, periods, slope_period, lags):
        """Calculate the slope of both SMA and EMA for each period in periods"""
        for period in periods:
            self.df[f'sma_slope_{period}'] = self.calculate_slope(self.df[f'sma_{period}'], slope_period)
            self.df[f'ema_slope_{period}'] = self.calculate_slope(self.df[f'ema_{period}'], slope_period)
        return self
    

    def add_technical_indicators(self, periods, slope_period = 5):
        self.calculate_rsi()
        self.calculate_rsi(window=2)
        self.calculate_macd()
        self.calculate_log_return(lags)
        self.calculate_return()
        self.calculate_roc()
        self.calculate_stoch()
        self.calculate_adx()
        self.calculate_hl_mean()
        self.calculate_lower_band()
        self.calculate_atr()
        self.calculate_ibs()
        self.calculate_obv()
        self.calculate_moving_averages(periods)
        # self.calculate_moving_average_slopes(periods, slope_period)
        return self.df

    
    


