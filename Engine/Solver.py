import numpy as np
from Engine.Functions import F
from Engine.Settings import Settings

class Solver:
    @staticmethod
    def rk4_step(y, h):
        """Performs a single step of the RK4 algorithm."""
        k1 = h * F.calculate_derivatives(y)
        k2 = h * F.calculate_derivatives(y + k1 / 2)
        k3 = h * F.calculate_derivatives(y + k2 / 2)
        k4 = h * F.calculate_derivatives(y + k3)
        return y + (k1 + 2*k2 + 2*k3 + k4) / 6

    @staticmethod
    def solve_ode(y0, t0, tf, dt):
        """Solves the ODE using RK4 from t0 to tf with initial conditions y0."""
        t_values = np.arange(t0, tf + dt, dt)
        state = y0
        
        for i in range(1, len(t_values)):
            state = Solver.rk4_step(state, dt)
            
            #stop if the object is not moving
            if(Solver.stop_moving_check(state)):
                return state
        
        return state
    
    @staticmethod
    def stop_moving_check(state):
        condition1 = abs(state[2]) < Settings.epsilon and abs(state[3]) < Settings.epsilon
        static_friction_force = F.static_friction_force(state)
        sliding_force = F.sliding_force(state)
        condition2 = static_friction_force[0] > sliding_force[0] and static_friction_force[1] > sliding_force[1]
        return condition1 & condition2