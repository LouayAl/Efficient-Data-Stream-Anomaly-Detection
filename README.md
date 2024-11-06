# Efficient-Data-Stream-Anomaly-Detection

 Python script capable of detecting anomalies in a continuous data stream. This stream, simulating real-time sequences of floating-point numbers, could represent various metrics such as financial transactions or system metrics. Your focus will be on identifying unusual patterns, such as exceptionally high values or deviations from the norm.

## Overview

The algorithm combines **Seasonal-Trend Decomposition (STL)** and **Z-score** calculations to effectively separate trend, seasonal, and residual components, and then analyze the residuals for anomalous behavior. This approach is particularly suitable for real-time anomaly detection due to its adaptability to non-stationary data and ability to detect sudden deviations without requiring extensive historical data. Additionally, it uses a sliding window to maintain efficient memory usage and allow for dynamic data stream processing.

### Why STL and Z-Score?

1. **STL Decomposition** :
   * **Seasonal-Trend decomposition** is a robust method to decompose the time series data into  **trend, seasonal, and residual components** .
   * By isolating these components, we can analyze the residual (random noise) directly for anomalies, which minimizes the impact of regular seasonal or trend patterns on anomaly detection.
   * STL is ideal for non-stationary data where both the trend and seasonality may evolve over time, making it well-suited for real-world data streams.
2. **Z-Score for Anomaly Detection** :
   * The **Z-score** is a statistical measure of how far a data point is from the mean in terms of standard deviations.
   * By calculating the Z-score of the residual component, we can assess if a point is significantly deviating from normal behavior.
   * A high Z-score (exceeding a threshold) signals an anomaly, such as an unusually high spike or drop in value.

## Program Workflow

1. **Data Generation** :
   * Simulated data points are generated with components for  **trend** ,  **seasonality** , and  **noise** , including an option to introduce anomalies.
   * Anomalies can be generated at a specified rate (`p`) by applying a significant deviation to randomly chosen points in the sequence.
2. **Anomaly Detection** :
   * For each incoming data point, the **sliding window** of recent points is maintained.
   * Once the sliding window is filled, **STL decomposition** is applied to extract the residual component.
   * The **Z-score** of the most recent residual is calculated, and if it exceeds the specified threshold, it is flagged as an anomaly.
3. **Real-Time Plotting** :
   * The data is plotted in real-time to visualize trends, seasonal patterns, and detected anomalies.
   * Detected anomalies are marked on the plot, allowing for dynamic monitoring of the data stream.

## Usage

1. **Run the Program** :To start the program and begin generating the data stream, run:

   ```
   python  visualize.py
   ```
2. **Parameters to Adjust** :

* **`window_size`** : Defines the size of the sliding window. It affects how much recent data is used for STL decomposition. Increasing the size smooths out short-term noise but may delay anomaly detection.
* **`z_threshold`** : Z-score threshold for classifying anomalies. A lower threshold makes the detector more sensitive to smaller deviations, while a higher threshold detects only more extreme anomalies.
* **`Amp`** and  **`T`** : Control the amplitude and period of the seasonal component, respectively. Adjusting these can simulate different seasonal cycles and magnitudes.
* **`p` (in `generate_data_point_with_anomalies`)** : Controls the proportion of data points that will be anomalies. Higher values increase the number of simulated anomalies.


## Real-Time Plotting


The program continuously appends new data to the plot, updating in real-time:

1. Each data point is plotted as it arrives, showing the trend and seasonal patterns.
2. Anomalies are marked distinctly, allowing easy visualization of unusual events.
3. The plot automatically updates at each interval, providing a real-time view of the data stream.


## Code Structure

### Key Functions

* **`trend(t)`** : Models the trend component.
* **`seasonality(t)`** : Models the seasonal component using a sinusoidal function.
* **`generate_data_points(num)`** : Generates data with combined trend, seasonality, and noise.
* **`generate_data_point_with_anomalies(num, p)`** : Introduces anomalies into the generated data.
* **`stl_zscore_anomaly_detection`** : Analyzes a batch of data for anomalies using STL decomposition and Z-score.
* **`stl_zscore_anomaly_detection_live`** : Performs real-time anomaly detection for each incoming data point.


### Real-Time Anomaly Detection Example

The `stl_zscore_anomaly_detection_live` function uses a sliding window and only returns **True** if the latest data point is an anomaly based on the Z-score threshold.

## Sample Output

The program provides:

* A **real-time plot** with detected anomalies highlighted.
* **Log output** with messages indicating errors or detected anomalies.
