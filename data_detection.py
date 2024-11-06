import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from statsmodels.tsa.seasonal import STL
import logging
# Configure logging for informational messages
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Define constants for amplitude and seasonal period
Amp = 10
T = 200

# Define the trend function as a logarithmic growth
def trend(t):
    return Amp*np.log(1+(Amp/T * t)) 
        
# Define the seasonality function with a sinusoidal pattern
def seasonality(t):
    return Amp * np.sin(2 * np.pi * t / T)  # Seasonal cycle

# Define the noise function to generate random noise
def noise(size):
    return np.random.normal(0, 0.1*Amp, size)  # Random noise with mean 0 and standard deviation scaled to amplitude

# Generate data points with trend, seasonality, and noise combined
def generate_data_points(num):
    t = np.arange(num)
    return trend(t) + seasonality(t) + noise(num)

# Function to generate data points with random anomalies added
def generate_data_point_with_anomalies(num,p):
    """
    Generates data points with a specified proportion of anomalies.

    Parameters:
    - num: int, total number of data points to generate.
    - p: float, proportion of data points to make anomalous.

    Returns:
    - data_points: array of data points including anomalies.
    - anomalies_indices: array of indices where anomalies were inserted.
    """
    data_points = generate_data_points(num)
    # create the anomalies 
    anomalies_num = int(p*num) # Calculate the number of anomalies to insert
    anomalies_values = 1.5*Amp # Set anomaly amplitude

    # Randomly select indices for anomalies, avoiding the start of the series
    anomalies_indices = np.random.permutation(np.arange(200,num))[:anomalies_num]
    data_points[anomalies_indices] += anomalies_values * (((data_points[anomalies_indices] - data_points[anomalies_indices-1])>=0)*2-1)
    
    
    return data_points, anomalies_indices


def stl_zscore_anomaly_detection(data_stream, window_size=1000, z_threshold=3):
    """
    Analyzes a data stream for anomalies using STL decomposition and Z-score.

    Parameters:
    - data_stream: list of incoming data points.
    - window_size: int, number of recent data points for STL decomposition.
    - z_threshold: float, threshold for Z-score to classify anomalies.

    Returns:
    - anomaly_indices: list of indices where anomalies were detected.
    - anomaly_scores: list of Z-scores for the anomalies.
    - anomaly_count: total number of detected anomalies.
    """

    data_window = [] # Sliding window to store recent data points
    anomaly_indices = [] # Indices of detected anomalies
    anomaly_scores = [] # Z-scores of detected anomalies
    anomaly_count = 0 # Counter for anomalies
    date_indexes = pd.date_range(start='1/1/2020', periods=window_size, freq='ms') # Generate timestamps
    
    
    for index, data_point in enumerate(data_stream):
        # Append the new data point to the sliding window
        data_window.append(data_point)
        
        # Keep the window within the specified size by removing oldest points
        if len(data_window) > window_size:
            data_window.pop(0)
        
        # Perform STL and Z-score analysis when window is full
        if len(data_window) == window_size:
            try:
                # Convert data to DataFrame for STL decomposition
                df = pd.DataFrame(data_window)
                df.index = date_indexes
                stl = STL(df)
                result = stl.fit()
                residual = result.resid # Obtain residual (noise component)

                # Calculate Z-Score for the residual
                mean_resid = np.mean(residual)
                std_resid = np.std(residual)
                z_scores = (residual - mean_resid) / std_resid
                
                # Check if latest Z-score exceeds the threshold for anomaly detection
                if abs(z_scores.iloc[-1]) > z_threshold:
                    data_window.pop() # Remove the anomaly point to avoid repetition
                    anomaly_count += 1 # Increment the count
                    anomaly_indices.append(index) # Save anomaly index
                    anomaly_scores.append(z_scores.iloc[-1]) # Save Z-score for analysis
                    
            except Exception as e:
                logging.error(f"Error in STL decomposition or Z-Score calculation: {e}")



    return anomaly_indices, anomaly_scores, anomaly_count

# Real-time anomaly detection with sliding window approach
def stl_zscore_anomaly_detection_live(data,data_window=[], window_size=200, z_threshold=3):
    """
    Real-time STL-based anomaly detection function.

    Parameters:
    - data: new incoming data point.
    - data_window: list, holds recent data points for STL.
    - window_size: int, window size for STL decomposition.
    - z_threshold: float, threshold for Z-score anomaly detection.

    Returns:
    - bool: True if current data point is an anomaly, else False.
    """
    
    date_indexes = pd.date_range(start='1/1/2020', periods=window_size, freq='ms') # Timestamps for the window
    data_window.append(data) # Add new data point to window
    
    # Keep the window within specified size by removing oldest data points
    if len(data_window) > window_size:
        data_window.pop(0)
    
    # Perform STL and Z-score analysis when window is full
    if len(data_window) == window_size:
        # Perform STL decomposition
        try:
            # Convert data to DataFrame for STL decomposition
            df = pd.DataFrame(data_window) 
            df.index = date_indexes
            stl = STL(df)
            result = stl.fit()
            residual = result.resid # Extract residuals for anomaly check

            # Calculate Z-Score for the residual
            mean_resid = np.mean(residual)
            std_resid = np.std(residual)
            z_scores = (residual - mean_resid) / std_resid
            # Check if latest data point's Z-score exceeds the threshold
            if abs(z_scores.iloc[-1]) > z_threshold:
                data_window.pop()
                return True
                
        except Exception as e:
            logging.error(f"Error in STL decomposition or Z-Score calculation: {e}")
    
    return False # No anomaly detected
