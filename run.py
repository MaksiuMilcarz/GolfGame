import matplotlib.pyplot as plt
import numpy as np
from Engine.Solver import Solver
from Engine.Settings import Settings
from Engine.Functions import F

def main():
    y0 = (-1.5, 0, 0, 1) # [x, y, Vx, Vy]
    t0 = Settings.t0  # Initial time
    t1 = Settings.t1  # Final time
    dt = Settings.dt  # Time step
    
    state = Solver.solve_ode(y0, t0, t1, dt)
    print()
    print("x1(t) = ", state[0], "   Vx1(1) = ", state[2])
    print("y1(t) = ", state[1], "   Vy1(1) = ", state[3])
    print()

if __name__ == "__main__":
    main()