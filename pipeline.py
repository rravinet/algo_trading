# %%
import pandas as pd
import yaml
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.graph_objects as go
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import ta
from algo_trading.log_config import setup_logging
from Fin_Database.Data.connect import engine, DailyStockData, HourlyStockData, OneMinuteStockData, FiveMinuteStockData,FifteenMinuteStockData, StockSplits, StockNews, CompanyFinancials
from algo_trading.Pre_Processing.pre_processing import PreProcessing
from algo_trading.Feature_Engineering.feature_engineering import TechnicalIndicators
from algo_trading.data_fetcher import DataFetcher


# %%
class Pipeline:
    def __init__(self, tickers, config_file= '../config.yaml'):
        if isinstance(tickers,str):
            self.tickers = [tickers]
        else:
            self.tickers = tickers
        
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.periods = self.config['technical_indicators']['fast_periods'] + self.config['technical_indicators']['slow_periods']
            
        
    def fetch_data(self, start_date = None, end_date = None, 
                   timespan = 'daily', combine = False):
        fetcher = DataFetcher(self.tickers)
        data = fetcher.get_stock_data(timespan = timespan, start_date = start_date, end_date = end_date, combine = combine)
        return data
    
    def preprocess_data(self, data, timespan):
        if isinstance(data, dict):
            preprocessed_data = {}
            for ticker, df in data.items():
                preprocessed_data[ticker] = PreProcessing(df, timespan).pre_processor().df
            return preprocessed_data
        else:
            return PreProcessing(data, timespan).pre_processor().df
    
    def feature_engineering(self, data, clean=False):
        if isinstance(data, dict):
            engineered_data = {}
            for ticker, df in data.items():
                fe = TechnicalIndicators(df)
                fe.add_technical_indicators(periods=self.periods)
                if clean:
                    fe.df.dropna(inplace=True)
                engineered_data[ticker] = fe.df
            return engineered_data
        else:
            fe = TechnicalIndicators(data)
            fe.add_technical_indicators(periods=self.periods)
            if clean:
                fe.df.dropna(inplace=True)
            return fe.df
    
    def pipeline(self, start_date = None, end_date = None, 
                 timespan = 'daily', combine = False, 
                 clean = False):
        
        data = self.fetch_data(start_date=start_date, end_date=end_date, timespan=timespan, combine=combine)
        preprocessed_data = self.preprocess_data(data, timespan)
        final_data = self.feature_engineering(preprocessed_data, clean=clean)
        return final_data
    
    


