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


class StockFeatures:
    %
# 
# # %%
class features:
    def __init__(self, df):
        self.df = df
    
    def date_features(self):
        self.df['day'] = self.df['date'].dt.day
        self.df['month'] = self.df['date'].dt.month
        self.df['day_of_week'] = self.df['date'].dt.dayofweek
        return self.df
    # add date/time to next corporate announcement
    
    


