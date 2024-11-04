import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
import logging
from data_stream import *

# Set up logging for tracking data generation and anomaly detection
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def stl_zscore_anomaly_detection(data_stream, window_size=300, seasonal_period=100, z_threshold=3):
    """
    Detects anomalies in a data stream using STL decomposition and Z-Score.

    Parameters:
    - data_stream: list or iterable of incoming data points (float values).
    - window_size: int, the number of most recent data points to use for each STL decomposition.
    - seasonal_period: int, estimated period for seasonality (e.g., 12 for monthly data if the data is daily).
    - z_threshold: float, Z-Score threshold for flagging anomalies.

    Returns:
    - anomalies: list of tuples (index, value) where anomalies were detected.
    """
    # Store data points and anomalies
    data_window = []
    anomalies = []

    for index, data_point in enumerate(data_stream):
        # Append the new data point to the sliding window
        data_window.append(data_point)
        
        # Maintain only the latest `window_size` points in the sliding window
        if len(data_window) > window_size:
            data_window.pop(0)
        
        # Proceed only when the sliding window is full
        if len(data_window) == window_size:
            # Perform STL decomposition
            try:
                stl = STL(pd.Series(data_window), seasonal=seasonal_period)
                result = stl.fit()
                residual = result.resid

                # Calculate Z-Score for the residual
                mean_resid = np.mean(residual)
                std_resid = np.std(residual)
                z_scores = (residual - mean_resid) / std_resid

                # Check the most recent data point's Z-Score for anomaly
                if abs(z_scores[-1]) > z_threshold:
                    logging.info(f"Anomaly detected at index {index}: {data_point} (Z-Score: {z_scores[-1]:.2f})")
                    anomalies.append((index, data_point))
                    
            except Exception as e:
                logging.error(f"Error in STL decomposition or Z-Score calculation: {e}")

        # Log data generation at each step
        logging.info(f"Data point {index}: {data_point}")

    return anomalies



def data_stream_with_anomalies2(num):
    t = 0
    arr = np.zeros((num,2))
    for i in range(num):
        arr[i][0],arr[i][1] = generate_data_point_with_anomalies(t)
    return arr


# # Simulated data stream with seasonal patterns and injected anomalies
# np.random.seed(42)
# data_stream = np.sin(np.linspace(0, 20, 500)) + np.random.normal(0, 0.5, 500)
# data_stream[100] = 5  # Inject a large anomaly
# data_stream[300] = -3  # Inject a negative anomaly

# # Run the anomaly detection
# anomalies = stl_zscore_anomaly_detection(data_stream_with_anomalies2(1000000), window_size=300, seasonal_period=100, z_threshold=3)

# print("Detected anomalies at indices and values:", anomalies)
