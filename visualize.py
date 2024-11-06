import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from data_detection import *

# Generate simulated data points with anomalies for testing
data_points, anomalies_indecies = generate_data_point_with_anomalies(1000,0.02) # 2% anomalies in 1000 point
WINDOW = [] # Initialize an empty window for real-time anomaly detection

# Generate initial data
# Initialize lists for tracking x and y data
x_data = []
y_data = []

# Initialize the figure and axis for plotting
fig, ax = plt.subplots()
 # Line plot for true normal data points ('TN')
line, = ax.plot([], [], 'b-', lw=2,label = "TN")  # 'b-' makes a blue line

# Initialize lists to store True Positives (TP), False Positives (FP), and False Negatives (FN)
TP = []
FP = []
FN = []

# Scatter plots for anomalies detected (True Positive, False Positive, and False Negative)
TP_scatter = ax.scatter([], [], color='green', label='TP')
FP_scatter = ax.scatter([], [], color='red', label='FP')
FN_scatter = ax.scatter([], [], color='black', label='FN')
# Add a legend to the figure
fig.legend(loc="upper right")

# Set up initial axis limit for the plot
ax.set_xlim(0, 100)  # Adjust x-axis limits for real-time visualization window
ax.set_ylim(-10, 10)  # Adjust y-axis limits based on data range
ax.set_title("Real-Time Data Stream")
ax.set_xlabel("Time")
ax.set_ylabel("Value")

def init():
    """Initialize the line plot for animation. Sets initial empty data."""
    line.set_data([], [])
    return line,


def update(frame):
    """
    Update function for each new data point
    - Detects anomalies
    - Adjusts plot limits if necessary
    - Updates line plot and scatter plots with new data.
    """
    
    draw = False # Flag to control if plot needs redrawing
    
    # Detect if the current data point (data_points[frame]) is an anomaly
    anomaly = stl_zscore_anomaly_detection_live(data_points[frame], WINDOW, 100, 3)
    
    # Append new data pointsto x and y data lists
    x_data.append(frame)
    y_data.append(data_points[frame])  
    
    # Update the line with new data
    line.set_data(x_data, y_data)
    
    # Slide the x-axis window to keep the latest data visible
    if len(x_data) > ax.get_xlim()[1]:
        
        # change the limits of the x-axis
        ax.set_xlim(0, len(x_data)+100)  # Shift x-axis as data grows
        
        # change also the write limit of the x-axis
        draw = True
        
    # Adjust y-axis dynamically if new data goes out of current y-axis limits
    if np.min(y_data) < ax.get_ylim()[0] + 5:
        ax.set_ylim(np.min(y_data) - 20, ax.get_ylim()[1])
        draw = True
    if np.max(y_data) > ax.get_ylim()[1] - 5:
        ax.set_ylim(ax.get_ylim()[0], np.max(y_data) + 20)
        draw = True
    
    # Track true positives (TP), false positives (FP), and false negatives (FN)
    if frame in anomalies_indecies:
        if anomaly: # If detected as an anomaly correctly
            TP.append(frame)
            scatter_points = np.column_stack((TP, data_points[TP]))
            TP_scatter.set_offsets(scatter_points)
        else: # Missed anomaly, mark as false negative
            FP.append(frame)
            scatter_points = np.column_stack((FP, data_points[FP]))
            FP_scatter.set_offsets(scatter_points)
    else:
        if anomaly: # Incorrectly flagged as an anomaly
            FN.append(frame)
            scatter_points = np.column_stack((FN, data_points[FN]))
            FN_scatter.set_offsets(scatter_points)
    
    # Redraw plot if axis limits were adjusted
    if draw:
        ax.figure.canvas.draw()
    
        
    return line,TP_scatter,FP_scatter,FN_scatter

# Use FuncAnimation to animate the plot in real-time
# 'frames' iterates over the range of data points
# 'interval' sets the delay between frames (in milliseconds)
ani = FuncAnimation(fig, update, frames=np.arange(0, len(data_points)), init_func=init, blit=True,repeat = False, interval=1)

# Display the real-time data stream plot with anomalies marked
plt.show()