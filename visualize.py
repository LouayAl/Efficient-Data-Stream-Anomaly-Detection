import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from data_detection import *

data_points, anomalies_indecies = generate_data_point_with_anomalies(1000,0.02)
WINDOW = []

# Generate initial data
x_data = []
y_data = []

# Initialize the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', lw=2,label = "TN")  # 'b-' makes a blue line


TP = []
FP = []
FN = []
TP_scatter = ax.scatter([], [], color='green', label='TP')
FP_scatter = ax.scatter([], [], color='red', label='FP')
FN_scatter = ax.scatter([], [], color='black', label='FN')
fig.legend(loc="upper right")

# Set up the plot limits
ax.set_xlim(0, 100)  # Adjust x-axis limits as needed
ax.set_ylim(-10, 10)  # Adjust y-axis limits as needed
ax.set_title("Real-Time Data Stream")
ax.set_xlabel("Time")
ax.set_ylabel("Value")

def init():
    """Initialize the line plot for animation"""
    line.set_data([], [])
    return line,


def update(frame):
    """Update function for each new data point"""
    draw = False
    # detect if data points[frame] is an anomaly 
    anomaly = stl_zscore_anomaly_detection_live(data_points[frame], WINDOW, 100, 3)
    
    # Append new data points
    x_data.append(frame)
    y_data.append(data_points[frame])  
    # Update the line with new data
    line.set_data(x_data, y_data)
    
    # Keep the data visible
    if len(x_data) > ax.get_xlim()[1]:
        # change the limits of the x-axis
        ax.set_xlim(0, len(x_data)+100)  # Slide the window to the right
        # change also the write limit of the x-axis
        draw = True
    # do the same for the y-axis
    if np.min(y_data) < ax.get_ylim()[0] + 5:
        ax.set_ylim(np.min(y_data) - 20, ax.get_ylim()[1])
        draw = True
    if np.max(y_data) > ax.get_ylim()[1] - 5:
        ax.set_ylim(ax.get_ylim()[0], np.max(y_data) + 20)
        draw = True
    
    if frame in anomalies_indecies:
        if anomaly:
            TP.append(frame)
            scatter_points = np.column_stack((TP, data_points[TP]))
            TP_scatter.set_offsets(scatter_points)
        else:
            FP.append(frame)
            scatter_points = np.column_stack((FP, data_points[FP]))
            FP_scatter.set_offsets(scatter_points)
    else:
        if anomaly:
            FN.append(frame)
            scatter_points = np.column_stack((FN, data_points[FN]))
            FN_scatter.set_offsets(scatter_points)
            

    
    
    
    
    
    
    # if axies are changed, draw the plot
    if draw:
        ax.figure.canvas.draw()
    
        
    return line,TP_scatter,FP_scatter,FN_scatter

# Use FuncAnimation to update the plot in real-time
ani = FuncAnimation(fig, update, frames=np.arange(0, len(data_points)), init_func=init, blit=True,repeat = False, interval=1)

# Display the plot
plt.show()