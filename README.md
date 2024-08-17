# Algo Trading - Under Developement

This project implements an** ****algorithmic trading pipeline** that fetches financial data from a SQL database, preprocesses it, applies feature engineering techniques, and prepares the data for algorithmic trading and strategy execution.

## Workflow

### 1. Fetching Data

The pipeline uses the** ****`DataFetcher` class** in** **`data_fetcher.py` to fetch stock data from the SQL database. This data is pulled from the tables that were populated by the** **`fin_database` project.

### 2. Preprocessing Data

After fetching the data, the pipeline preprocesses it using the** ****`PreProcessing` class** in** **`pre_processing.py`. This may involve:

* **Filtering Market Hours** : Ensuring that only market trading hours are included.
* **Setting Indexes** : Setting the appropriate date/time columns as the index for time series analysis.
* 

### 3. Feature Engineering

Next, the pipeline applies various feature engineering techniques using the** ****`TechnicalIndicators` class** in** **`feature_engineering.py`. These techniques include adding:

* Moving averages
* Relative Strength Index (RSI)
* Bollinger Bands
* Other technical indicators

### 4. Volatility Prediction

Intraday Volatility prediction using the** ****`IntradayVol`**** class in `vol_prediction.py`. Here I am applying the methodology from Young Li's paper titled 

"A PRACTICAL MODEL FOR PREDICTION OF INTRADAY
VOLATILITY"

### 5. Final Output

The pipeline returns either a single processed DataFrame or a dictionary of processed DataFrames (one per ticker), which can then be used for strategy development and execution.
