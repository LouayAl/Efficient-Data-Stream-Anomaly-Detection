import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Generate initial data
x_data = []
y_data = []

# Initialize the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', lw=2)  # 'b-' makes a blue line
scatter = ax.scatter([], [], color='red')  # Scatter plot for red points

TP = []
FP = []
TN = []
FN = []

# Set up the plot limits
ax.set_xlim(0, 100)  # Adjust x-axis limits as needed
ax.set_ylim(-10, 10)  # Adjust y-axis limits as needed
ax.set_title("Real-Time Data Stream")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
c= 0
def init():
    """Initialize the line plot for animation"""
    line.set_data([], [])
    return line,
scatter_points = 0
def update(frame):
    """Update function for each new data point"""
    # Append new data points
    x_data.append(frame)
    y_data.append(np.sin(frame / 10) + np.random.normal(scale=0.5) + frame)  # Sine wave with noise
    # Keep the data visible
    if len(x_data) > 100:
        # change the limits of the x-axis
        ax.set_xlim(0, len(x_data))  # Slide the window to the right
        # change also the write limit of the x-axis
        ax.figure.canvas.draw()
    global scatter_points
    if frame == 50 :
        scatter_points = np.column_stack((x_data[-10:], y_data[-10:]))  # Last 10 points as red dots
        scatter.set_offsets(scatter_points)
    if frame == 100:
        # add another 10 points to the scatter_points
        scatter_points = np.concatenate((scatter_points, np.column_stack((x_data[-10:], y_data[-10:]))))
        scatter.set_offsets(scatter_points)
    
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
ani = FuncAnimation(fig, update, frames=np.arange(0, 1000), init_func=init, blit=True, interval=10)

# Display the plot
plt.show()