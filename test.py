import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from data_detection import *

data_points, anomalies_indecies = generate_data_point_with_anomalies(300,0.02)
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

scatter_points = 0

def update(frame):
    """Update function for each new data point"""
    
    # Append new data points
    x_data.append(frame)
    y_data.append(data_points[frame])  
    # Keep the data visible
    if len(x_data) > 100:
        # change the limits of the x-axis
        ax.set_xlim(0, len(x_data))  # Slide the window to the right
        # change also the write limit of the x-axis
        ax.figure.canvas.draw()
    
    
     
    
    
    # do the same for the y-axis
    if np.min(y_data) < ax.get_ylim()[0] + 5:
        ax.set_ylim(np.min(y_data) - 5, ax.get_ylim()[1])
    if np.max(y_data) > ax.get_ylim()[1] - 5:
        ax.set_ylim(ax.get_ylim()[0], np.max(y_data) + 5)
    ax.figure.canvas.draw()
    
        
        
        

    # Update the line with new data
    line.set_data(x_data, y_data)
    

    return line,

# Use FuncAnimation to update the plot in real-time
ani = FuncAnimation(fig, update, frames=np.arange(0, len(data_points)), init_func=init, blit=True,repeat = False, interval=100)

# Display the plot
plt.show()