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
from algo_trading.Feature_Engineering.feature_engineering import TechnicalIndicators



class IntraBarsProfile:
    def __init__(self, hf_df, lf_df, daily_df, timespan):
        """args:
        hf_df: higher frequency dataframe
        lf_df: lower frequency dataframe
        daily_df: daily dataframe
        timespan: timespan of the lower frequency data to aggregate : '15M', '1H', '1D', '1W....'"""
        self.hf_df = hf_df
        self.lf_df = lf_df
        self.daily_df = daily_df
        self.timespan = timespan
        
        
    def hurst(self):
        pass

# %%
class IntradayVol(IntraBarsProfile):
    def __init__(self, hf_df, lf_df, daily_df, timespan, decay_factor = 0.94):
        super().__init__(hf_df, lf_df, daily_df, timespan)
        self.decay_factor = decay_factor

    
    def calculate_daily_vol(self):
        """ Calculate daily vol using EWMA model """
        self.daily_df['daily_vol_squared'] = np.zeros(len(self.daily_df), dtype=float)
        
        self.daily_df['squared_log_ret'] = self.daily_df['log_ret'] ** 2
        self.daily_df['squared_log_ret'].bfill(inplace=True)

        for i in range(1, len(self.daily_df)):
            self.daily_df.loc[self.daily_df.index[i], 'daily_vol_squared'] = (
                self.decay_factor * self.daily_df['daily_vol_squared'].iloc[i-1] +
                (1 - self.decay_factor) * self.daily_df['squared_log_ret'].iloc[i]
            )
        
        return np.sqrt(self.daily_df['daily_vol_squared'])


    
    def calculate_diurnal_profile(self):
        """Calculate diurnal profile. Basically the average of the Garman-Klass vol for each time of the day. 
        It is calculated using the aggregated data of the higher frequency data"""
        aggregated_df = self.hf_df.groupby(self.hf_df.index.floor(self.timespan)).aggregate({'open': 'first', 
                                                               'high': 'max', 
                                                               'low': 'min', 
                                                               'close': 'last'})
        garma_klass_vol = np.sqrt(0.5*(np.log(aggregated_df['high']) - np.log(aggregated_df['low']))**2 - (2 * np.log(2) -1) * (np.log(aggregated_df['close']) - np.log(aggregated_df['open']))**2)
        q25 = garma_klass_vol.groupby(aggregated_df.index.time).quantile(0.25)
        q50 = garma_klass_vol.groupby(aggregated_df.index.time).quantile(0.5)
        q75 = garma_klass_vol.groupby(aggregated_df.index.time).quantile(0.75)
        
        diurnal_profile = (q25 + q50 + q75) / 3
        diurnal_profile = diurnal_profile / diurnal_profile.mean()
        
        return diurnal_profile
    
    
    def predict_vol(self):
        """ Predict vol for the next time interval"""
        daily_vol = self.calculate_daily_vol().shift(1)
        diurnal_profile = self.calculate_diurnal_profile()
        avg_diurnal_profile = diurnal_profile.mean()
        
        # time-scaling factor (rho_t)
        time_scaling_factor = 1 

        self.lf_df['vol_forecasts'] = np.nan
        for i in range(len(self.lf_df)):
            current_time = self.lf_df.index[i].time()
            current_date = self.lf_df.index[i].date()
            
            daily_vol_value = daily_vol.loc[pd.Timestamp(current_date)]
            if current_time in diurnal_profile.index:
                self.lf_df.loc[self.lf_df.index[i], 'vol_forecasts'] = (
                    daily_vol_value * time_scaling_factor * (diurnal_profile[current_time] / avg_diurnal_profile)
                )
            else:
                self.lf_df.loc[self.lf_df.index[i], 'vol_forecasts'] = np.nan
        return self.lf_df


    
    



