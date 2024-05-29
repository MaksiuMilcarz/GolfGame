from dataclasses import dataclass

@dataclass
class Settings:
    m: float = 1
    g: float = 9.81
    dt: float = 0.01
    t0: float = 0
    t1: float = 1
    kinetic_friction_coefficient: float = 0.1
    static_friction_coefficient: float = 0.2
    epsilon: float = 0.01

    