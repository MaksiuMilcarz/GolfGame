import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from Engine.Functions import F
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageTk

class GolfSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Golf Simulation")
        
        # Create a frame to hold both the canvas and the button panel
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons panel on the left
        self.buttons_frame = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.button_plot = tk.Button(self.buttons_frame, text="Plot Map", command=self.plot_map)
        self.button_plot.pack(pady=10)

        # Create main canvas in the center
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize variables to hold the background image
        self.map_image = None
        self.map_photo = None

    def plot_map(self):
        # Define the range of x and y coordinates
        x_range = np.linspace(-10, 10, 1000)
        y_range = np.linspace(-10, 10, 1000)

        # Create a meshgrid for x and y coordinates
        X, Y = np.meshgrid(x_range, y_range)

        # Calculate height values for each (x, y) coordinate using the height function
        Z = F.height_function(X, Y)

        # Convert the height map array to an image
        height_map_image = Image.fromarray((Z * 255 / np.max(Z)).astype(np.uint8))

        # Convert the image to tkinter-compatible format
        self.map_photo = ImageTk.PhotoImage(height_map_image)

        # Display the height map as background on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

def main():
    root = tk.Tk()
    app = GolfSimulationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
