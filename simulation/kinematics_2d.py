import numpy as np

class Kinematics2D:
    def __init__(self, x0, y0, vx0, vy0, ax, ay):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0
        self.ax = ax
        self.ay = ay

    def position(self, t):
        # (x, y) at time t (as two arrays)
        x = self.x0 + self.vx0 * t + 0.5 * self.ax * t ** 2
        y = self.y0 + self.vy0 * t + 0.5 * self.ay * t ** 2
        return x, y

    def velocity(self, t):
        vx = self.vx0 + self.ax * t
        vy = self.vy0 + self.ay * t
        return vx, vy
