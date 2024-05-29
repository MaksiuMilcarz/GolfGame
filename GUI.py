import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from Engine.Functions import F
from Engine.Solver import Solver
from Engine.Settings import Settings
import matplotlib.pyplot as plt

class GolfSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Golf Simulation")
        
        # Determine screen size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Calculate canvas size
        canvas_width = screen_width - 200  # Subtracting the width of the button panel
        canvas_height = screen_height
        
        # Create a frame to hold both the canvas and the button panel
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create button panel on the left
        self.button_frame = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Button to create ball
        self.button_create_ball = tk.Button(self.button_frame, text="Create Ball", command=self.create_ball)
        self.button_create_ball.pack(pady=10)

        # Entry fields for ball position
        self.label_position = tk.Label(self.button_frame, text="Enter ball position:")
        self.label_position.pack()
        self.entry_x = tk.Entry(self.button_frame)
        self.entry_x.pack()
        self.entry_y = tk.Entry(self.button_frame)
        self.entry_y.pack()

        # Create main canvas in the center for background map
        self.map_canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height)
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize variables to hold the background image and ball object
        self.map_photo = None
        self.ball = None

        # Plot initial map
        self.plot_map()

    def plot_map(self):
        # Define the range of x and y coordinates
        x_range = np.linspace(-10, 10, 1000)
        y_range = np.linspace(-10, 10, 1000)

        # Create a meshgrid for x and y coordinates
        X, Y = np.meshgrid(x_range, y_range)

        # Calculate height values for each (x, y) coordinate using the height function
        Z = F.height_function(X, Y)

        # Normalize the height values to range from 0 to 1
        normalized_Z = (Z - np.min(Z)) / (np.max(Z) - np.min(Z))

        # Apply a colormap to represent height with varying intensities of green
        greens_colormap = plt.cm.get_cmap('Greens')
        greens_colors = (greens_colormap(normalized_Z) * 255).astype(np.uint8)

        # Create an RGBA image using the green colormap
        greens_image = Image.fromarray(greens_colors[:, :, :3], mode='RGB')

        # Convert the image to tkinter-compatible format for background map
        self.map_photo = ImageTk.PhotoImage(greens_image)

        # Display the height map as background on the map canvas
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)


    def draw_ball(self, position):
        # Clear previous ball
        if self.ball:
            self.map_canvas.delete(self.ball)

        # Draw new ball as a dot
        ball_radius = 10  # Adjust the size of the dot as needed
        ball_x, ball_y = position
        self.ball = self.map_canvas.create_oval(ball_x - ball_radius, ball_y - ball_radius,
                                                ball_x + ball_radius, ball_y + ball_radius,
                                                fill="red")

    def create_ball(self):
        # Get ball position from entry fields
        x = float(self.entry_x.get())
        y = float(self.entry_y.get())

        # Calculate canvas coordinates from world coordinates
        canvas_width = self.map_canvas.winfo_width()
        canvas_height = self.map_canvas.winfo_height()
        canvas_x = (x + 10) * canvas_width / 20  # Map x range [-10, 10] to canvas x range [0, canvas_width]
        canvas_y = canvas_height - (y + 10) * canvas_height / 20  # Map y range [-10, 10] to canvas y range [canvas_height, 0]

        # Draw the ball on the canvas
        self.draw_ball((canvas_x, canvas_y))



def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Set full screen mode
    app = GolfSimulationApp(root)
    app.plot_map()  # Plot initial map
    root.mainloop()

if __name__ == "__main__":
    main()
