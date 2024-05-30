import tkinter as tk
from Engine.Solver import Solver
from Engine.Settings import Settings

class Ball:
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color
        self.canvas_id = None

    def draw(self, app, canvas):
        x, y = app.convert_to_canvas_coords(self.position[0], self.position[1])
        if self.canvas_id:
            canvas.delete(self.canvas_id)
        self.canvas_id = canvas.create_oval(x - self.radius, y - self.radius,
                                             x + self.radius, y + self.radius,
                                             fill=self.color)

    def move(self, new_position, app, canvas):
        canvas.delete(self.canvas_id)
        self.position = new_position
        self.draw(app, canvas)
        
    def calculate_new_position(self, Vx, Vy, app, canvas):
        dt = Settings.dt  # Time step
        y0 = (self.position[0], self.position[1], Vx, Vy) # [x, y, Vx, Vy]

        state = Solver.solve_ode(y0, 0, 100, dt)

        self.move((state[0],state[1]), app, canvas)
