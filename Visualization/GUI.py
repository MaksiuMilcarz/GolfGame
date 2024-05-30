import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from Engine.Functions import F
from Visualization.Balls import Ball

class GolfSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Golf Simulation")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        canvas_width = (screen_width - 400) // 2  # Subtracting the width of the button panels
        canvas_height = screen_height

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        self.left_panel = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.label_target_position = tk.Label(self.left_panel, text="Enter target position:")
        self.label_target_position.pack(pady=(10, 0))
        self.entry_target_x = tk.Entry(self.left_panel)
        self.entry_target_x.pack()
        self.entry_target_y = tk.Entry(self.left_panel)
        self.entry_target_y.pack()
        self.button_create_target = tk.Button(self.left_panel, text="Create Target", command=self.create_target)
        self.button_create_target.pack(pady=10)

        self.label_position_p1 = tk.Label(self.left_panel, text="Enter Player 1 ball position:")
        self.label_position_p1.pack()
        self.entry_x_p1 = tk.Entry(self.left_panel)
        self.entry_x_p1.pack()
        self.entry_y_p1 = tk.Entry(self.left_panel)
        self.entry_y_p1.pack()
        self.button_create_ball_p1 = tk.Button(self.left_panel, text="Create Player 1 Ball", command=self.create_ball_p1)
        self.button_create_ball_p1.pack(pady=10)

        self.label_position_p2 = tk.Label(self.left_panel, text="Enter Player 2 ball position:")
        self.label_position_p2.pack()
        self.entry_x_p2 = tk.Entry(self.left_panel)
        self.entry_x_p2.pack()
        self.entry_y_p2 = tk.Entry(self.left_panel)
        self.entry_y_p2.pack()
        self.button_create_ball_p2 = tk.Button(self.left_panel, text="Create Player 2 Ball", command=self.create_ball_p2)
        self.button_create_ball_p2.pack(pady=10)

        # Right panel
        self.right_panel = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.label_velocity = tk.Label(self.right_panel, text="Enter new velocity:")
        self.label_velocity.pack(pady=(10, 0))
        self.entry_velocity_x = tk.Entry(self.right_panel)
        self.entry_velocity_x.pack()
        self.entry_velocity_y = tk.Entry(self.right_panel)
        self.entry_velocity_y.pack()

        self.button_hit = tk.Button(self.right_panel, text="Hit", command=self.hit_ball_p1)
        self.button_hit.pack(pady=10)

        self.map_canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height)
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.map_photo = None
        self.ball_p1 = None
        self.ball_p2 = None
        self.target = None

        self.plot_map()

    def plot_map(self):
        x_range = np.linspace(-10, 10, 1000)
        y_range = np.linspace(-10, 10, 1000)
        X, Y = np.meshgrid(x_range, y_range)
        Z = F.height_function(X, Y)

        Z_above_zero = np.clip(Z, 0, None)
        normalized_Z = (Z_above_zero - np.min(Z_above_zero)) / (np.max(Z_above_zero) - np.min(Z_above_zero))

        greens_colormap = plt.cm.get_cmap('Greens')
        greens_colors = (greens_colormap(normalized_Z) * 255).astype(np.uint8)

        height_image = np.zeros((Z.shape[0], Z.shape[1], 3), dtype=np.uint8)
        height_image[Z >= 0, :] = greens_colors[Z >= 0, :3]
        height_image[Z < 0, :] = [0, 0, 255]
        height_image_pil = Image.fromarray(height_image, mode='RGB')

        self.map_photo = ImageTk.PhotoImage(height_image_pil)
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

    def create_ball_p1(self):
        x = float(self.entry_x_p1.get())
        y = float(self.entry_y_p1.get())

        if not self.ball_p1:
            self.ball_p1 = Ball((x, y), radius=7, color="yellow")
        else:
            self.ball_p1.position = (x, y)

        self.ball_p1.draw(self, self.map_canvas)

    def create_ball_p2(self):
        x = float(self.entry_x_p2.get())
        y = float(self.entry_y_p2.get())

        if not self.ball_p2:
            self.ball_p2 = Ball((x, y), radius=7, color="white")
        else:
            self.ball_p2.position = (x, y)

        self.ball_p2.draw(self, self.map_canvas)

    def create_target(self):
        x = float(self.entry_target_x.get())
        y = float(self.entry_target_y.get())

        if not self.target:
            self.target = Ball((x, y), radius=10, color="red")
        else:
            self.target.position = (x, y)

        self.target.draw(self, self.map_canvas)
        
    def hit_ball_p1(self):
        velocity_x = float(self.entry_velocity_x.get())
        velocity_y = float(self.entry_velocity_y.get())
        self.ball_p1.calculate_new_position(velocity_x, velocity_y, self, self.map_canvas)

    def convert_to_canvas_coords(self, x, y):
        canvas_width = self.map_canvas.winfo_width()
        canvas_height = self.map_canvas.winfo_height()
        canvas_x = (x + 10) * canvas_width / 20  # Map x range [-10, 10] to canvas x range [0, canvas_width]
        canvas_y = canvas_height - (y + 10) * canvas_height / 20  # Map y range [-10, 10] to canvas y range [canvas_height, 0]
        return canvas_x, canvas_y