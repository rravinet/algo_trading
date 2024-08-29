# %%
import sys
import os

sys.path.append('/Users/raphaelravinet/Code')

import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime, timedelta
import logging
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from algo_trading.log_config import setup_logging
# from algo_trading.Data.data_fetching import 

# %%
setup_logging()

# %%
class PreProcessing:
    def __init__(self, df, timespan = 'daily'):
        self.df = df
        self.timespan = timespan
        
    def filter_market_hours(self):
        if self.timespan in ['minute', 'hour']:   
            df = self.df.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = df['date'].dt.time
            start_time = datetime.strptime('09:30', '%H:%M').time()
            end_time = datetime.strptime('16:00', '%H:%M').time()
            df = df[(df['time'] >= start_time) & (df['time'] <= end_time)]
            self.df = df.drop(columns=['time'])
        return self
    
    
    def setting_index(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.index = self.df['date']
        return self
    
    def pre_processor(self):
        self.filter_market_hours()
        self.setting_index()
        return self
    
    
        ###need to add pre processing steps for the financial news and company level data

    



