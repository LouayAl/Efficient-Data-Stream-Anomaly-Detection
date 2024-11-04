import numpy as np
import matplotlib.pyplot as plt
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Define the trend, seasonality, and noise functions
def trend(t):
    return 0.01 * t  # Linear trend

def seasonality(t):
    return 10 * np.sin(2 * np.pi * t / 100)  # Seasonal cycle

def noise():
    return np.random.normal(0, 2)  # Random noise with mean 0 and standard deviation 2

# Function to generate a data point with trend, seasonality, and noise
def generate_data_point(t):
    return trend(t) + seasonality(t) + noise()

# Function to generate data point with occasional anomalies
def generate_data_point_with_anomalies(t):
    base_value = generate_data_point(t)
    anomaly = False
    if np.random.rand() < 0.05:  # 5% chance of anomaly
        anomaly_value = np.random.choice([-1, 1]) * np.random.uniform(20, 40)
        base_value += anomaly_value
        anomaly = True
        logging.info(f"Time {t}: Anomaly detected with value {base_value:.2f}")
    else:
        logging.info(f"Time {t}: Normal value generated {base_value:.2f}")
    return base_value, anomaly

# Streaming data generator with anomalies
def data_stream_with_anomalies():
    t = 0
    while True:
        yield generate_data_point_with_anomalies(t)
        t += 1
        time.sleep(0.1)  # Adjust for stream speed (0.1s = 10 points per second)


# Collect and plot data with annotations for anomalies
def simulate_and_plot_stream(num_points=200):
    stream = data_stream_with_anomalies()
    data = []
    anomaly_points = []

    for _ in range(num_points):
        value, is_anomaly = next(stream)
        data.append(value)
        if is_anomaly:
            anomaly_points.append((_, value))  # Store index and value for anomalies

    # Plot the simulated data stream
    plt.figure(figsize=(14, 7))
    plt.plot(data, label="Data Stream", color="blue")
    
    # Plot anomalies in red
    if anomaly_points:
        anomaly_indices, anomaly_values = zip(*anomaly_points)
        plt.scatter(anomaly_indices, anomaly_values, color="red", label="Anomalies", zorder=5)
    
    # Add labels, title, and legend
    plt.title("Simulated Data Stream with Trend, Seasonality, and Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

    # Show descriptive annotations
    plt.annotate("Seasonal fluctuations", xy=(num_points/4, data[int(num_points/4)]), 
                 xytext=(num_points/4, max(data) + 10),
                 arrowprops=dict(facecolor='gray', shrink=0.05))
    plt.annotate("Trend over time", xy=(num_points/2, data[int(num_points/2)]), 
                 xytext=(num_points/2, min(data) - 10),
                 arrowprops=dict(facecolor='gray', shrink=0.05))
    
    # Display the plot
    plt.show()

# Run the simulation and plot
simulate_and_plot_stream()
