# ALGO_TRADING - Under Development

## Overview

This project implements an end-to-end pipeline for algorithmic trading, including data fetching, preprocessing, feature engineering, modeling, and strategy backtesting.

## Workflow

The workflow consists of the following steps:

1. **Data Fetching (`data_fetcher.ipynb`)**

   - Fetches and loads data from the `Fin_Database` repository stored in PostgreSQL into the project. The data is then used in subsequent steps of the pipeline.
2. **Preprocessing (`Pre_Processing/preprocessing.ipynb`)**

   - This step cleans the raw data by handling missing values, standardising formats, and transforming the data into a format ready for further processing. The cleaned data is then saved for the feature engineering stage.
3. **Feature Engineering (`Feature_Engineering/feature_engineering.ipynb`, `Feature_Engineering/vol_prediction.ipynb`)**

   - New features are created from the cleaned data, such as technical indicators, rolling statistics, and any other relevant metrics. The `vol_prediction.ipynb` notebook specifically focuses on predicting intraday volatility .
4. **Modelling (`Modelling/model.ipynb`)**

   - Predictive models such as decision trees, random forests, or gradient boosting machines are trained using the features generated in the previous step.
5. **Backtesting and Strategy Application (`Strategies/backtest_strategy.ipynb`)**

   - This notebook (currently under development) will perform backtests by applying the predictive models and trading strategies on historical data. The goal is to evaluate the efficacy of different trading strategies by simulating how they would have performed using past data.
6. **Signal Generation (`signal_generation.ipynb`)**

   - This notebook (currently under development) will generated signals from the trained models and strategies are produced, visualized, and analysed. These signals may include buy/sell/hold signals, position sizing, or other actionable insights based on the model's predictions.
