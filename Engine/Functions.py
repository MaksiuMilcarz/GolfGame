import numpy as np
from Engine.Settings import Settings

class F:
    @staticmethod
    def height_function(x, y):
        return 0.4 * np.sin(x*0.5) * np.cos(y*0.5) + 0.2
    
    @staticmethod
    def get_gradient(x, y):
        # Compute partial derivatives of the height function
        epsilon = Settings.dt
        dh_dx = (F.height_function(x + epsilon, y) - F.height_function(x - epsilon, y)) / (2 * epsilon)
        dh_dy = (F.height_function(x, y + epsilon) - F.height_function(x, y - epsilon)) / (2 * epsilon)
        return np.array([dh_dx, dh_dy])

    @staticmethod
    def calculate_derivatives(state):
        x, y, Vx, Vy = state
        Fx, Fy = F.get_forces(state)
        m = Settings.m
        
        dx_dt = Vx
        dy_dt = Vy
        dVx_dt = Fx / m
        dVy_dt = Fy / m
        
        return np.array([dx_dt, dy_dt, dVx_dt, dVy_dt])
    
    @staticmethod
    def get_forces(state):
        kinetic_friction_force = F.kinetic_friction_force(state)
        sliding_force = F.sliding_force(state)
        
        Fx = kinetic_friction_force[0] + sliding_force[0]
        Fy = kinetic_friction_force[1] + sliding_force[1]
        
        #print("slidingX: ", sliding_force[0], " frictionX: ", kinetic_friction_force[0])
        print("slidingY: ", sliding_force[1], " frictionY: ", kinetic_friction_force[1])  
        
        return Fx, Fy
    
    @staticmethod
    def gravity_force():
        m = Settings.m
        g = Settings.g
        Fy = -m * g
        return Fy

    @staticmethod
    def sliding_force(state):
        gradient = F.get_gradient(state[0], state[1])
        gravity_force = F.gravity_force()
        gradient_magnitude = np.linalg.norm(gradient)
        
        sliding_force_magnitude = gravity_force * gradient_magnitude
       
        slope_direction = gradient / gradient_magnitude
        
        sliding_fx = sliding_force_magnitude * slope_direction[0]
        sliding_fy = sliding_force_magnitude * slope_direction[1]
        return sliding_fx, sliding_fy
        
    @staticmethod
    def static_friction_force(state):
        [x, y, Vx, Vy] = state
        gravity = F.gravity_force()
        gradient = F.get_gradient(x, y)
        gradient_magnitude = np.linalg.norm(gradient)

        normal_force_magnitude = gravity / np.sqrt(1 + gradient_magnitude**2)

        static_friction_coefficient = Settings.static_friction_coefficient
        static_friction_force_magnitude = static_friction_coefficient * normal_force_magnitude

        slope_direction = gradient / gradient_magnitude
        
        static_friction_fx = -static_friction_force_magnitude * slope_direction[0]
        static_friction_fy = -static_friction_force_magnitude * slope_direction[1]
        return static_friction_fx, static_friction_fy

    @staticmethod
    def kinetic_friction_force(state):
        [x, y, Vx, Vy] = state
        m = Settings.m
        g = Settings.g
        v = np.array([Vx, Vy])
        v_magnitude = np.linalg.norm(v)

        if v_magnitude == 0:
            return 0, 0
        
        gradient = F.get_gradient(x, y)
        gradient_magnitude = np.linalg.norm(gradient)
        normal_force_magnitude = m * g / np.sqrt(1 + gradient_magnitude**2)
        
        kinetic_friction_coefficient = Settings.kinetic_friction_coefficient
        kinetic_friction_force_magnitude = kinetic_friction_coefficient * normal_force_magnitude

        friction_direction = -v / v_magnitude
        
        kinetic_friction_fx = kinetic_friction_force_magnitude * friction_direction[0]
        kinetic_friction_fy = kinetic_friction_force_magnitude * friction_direction[1]
        return kinetic_friction_fx, kinetic_friction_fy