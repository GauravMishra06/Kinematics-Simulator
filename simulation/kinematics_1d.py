import numpy as np

class Kinematics1D:
    def __init__(self, x0, v0, a):
        self.x0 = x0
        self.v0 = v0
        self.a = a

    def position(self, t):
        # x = x0 + v0*t + 0.5*a*t^2
        return self.x0 + self.v0 * t + 0.5 * self.a * t ** 2

    def velocity(self, t):
        # v = v0 + a*t
        return self.v0 + self.a * t
