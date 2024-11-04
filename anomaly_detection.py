from statsmodels.tsa.seasonal import STL
import numpy as np

# define a function which takes a list of numbers and returns the anomaly score of each number while implementing STL + Z-Score algorithm
def detect_anomalies(data, seasonality=10, trend=0.01, window=10, sigma=2):
    # Seasonal-Trend decomposition using LOESS
    stl = seasonal_decompose(data, period=seasonality, lo_frac=0.1, lo_delta=0.01)
    seasonal, trend, residual = stl.seasonal, stl.trend, stl.resid
    
    # Calculate the rolling mean and standard deviation of the residual
    rolling_mean = residual.rolling(window=window, min_periods=1, center=True).mean()
    rolling_std = residual.rolling(window=window, min_periods=1, center=True).std()
    
    # Calculate the Z-Score
    z_score = (residual - rolling_mean) / rolling_std
    
    # Identify anomalies based on the Z-Score
    anomalies = np.abs(z_score) > sigma
    
    return anomalies

def seasonal_decompose(data, period, lo_frac=0.1, lo_delta=0.01):
    # Initialize the seasonal-trend decomposition model
    stl = STL(data, period=period, lo_frac=lo_frac, lo_delta=lo_delta)
    
    # Fit the model to the data
    stl.fit()