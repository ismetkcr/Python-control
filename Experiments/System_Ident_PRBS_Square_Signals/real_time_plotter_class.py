import matplotlib.pyplot as plt
import time
import random
from matplotlib.colors import TABLEAU_COLORS  # For distinct colors

class EnhancedRealTimePlot:
    def __init__(self, data, x_key, y_keys, x_label, y_label, graph_size):
        self.data = data
        self.x_key = x_key
        self.y_keys = y_keys if isinstance(y_keys, (list, tuple)) else [y_keys]
        self.x_label = x_label
        self.y_label = y_label
        self.graph_size = graph_size
        self.colors = list(TABLEAU_COLORS.values())  # Predefined distinct colors

        plt.ion()  # Enable interactive mode
        self.fig, self.ax = plt.subplots()
        
        # Create multiple lines if needed
        self.lines = []
        for i, key in enumerate(self.y_keys):
            color = self.colors[i % len(self.colors)]
            line, = self.ax.plot([], [], color=color, label=key)
            self.lines.append(line)
            
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_title(f'{self.y_label} vs {self.x_label}')
        self.ax.legend(loc='upper right')
        self.ax.grid(True)  # Enable grid lines
        self.fig.canvas.draw()

    def update(self):
        if len(self.data) == 0:
            return

        # Get last N entries based on graph_size
        data_subset = self.data[-self.graph_size:]
        x_values = [entry[self.x_key] for entry in data_subset]
        
        # Update each line
        for i, key in enumerate(self.y_keys):
            y_values = [entry[key] for entry in data_subset]
            self.lines[i].set_xdata(x_values)
            self.lines[i].set_ydata(y_values)

        # Adjust axis limits
        self.ax.relim()
        self.ax.autoscale_view()

        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.close(self.fig)
