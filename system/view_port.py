import numpy as np


class ViewPort:

    def __init__(self, vpx, vpy, window) -> None:
        self.vpxmax = vpx
        self.vpymax = vpy
        self.vpxmin = 0
        self.vpymin = 0
        self.window = window

    def transform(self, x, y):
        wcmax = (self.window.wxmax, self.window.wymax)
        wcmin = (self.window.wxmin, self.window.wymin)
        vp_x = (((x - wcmin[0]) / (wcmax[0] - wcmin[0])) * (self.vpxmax - self.vpxmin))
        vp_y = ((1 - ((y - wcmin[1]) / (wcmax[1] - wcmin[1]))) * (self.vpymax - self.vpymin))
        return (vp_x, vp_y)

    def create_translation_matrix(self, dx, dy):
        return np.matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

    def create_scale_matrix(self, sx, sy):
        return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def create_rotation_matrix(self, angle):
        return np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
