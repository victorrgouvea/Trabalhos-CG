import numpy as np
from system.utils import create_normalized_matrix


class Window:

    def __init__(self, wx, wy) -> None:
        self.wxmin = -wx/2
        self.wymin = -wy/2
        self.wxmax = wx/2
        self.wymax = wy/2
        self.sizex = wx
        self.sizey = wy
        self.scale = [2/self.sizex, 2/self.sizey]
        self.center = [(self.wxmin + self.wxmax) / 2, (self.wymin + self.wymax) / 2]
        self.normalized_center = [0, 0]
        self.angle_offset = 0
        self.coordinates = [[self.wxmin, self.wymin, 1], [self.wxmax, self.wxmin, 1], [self.wxmax, self.wymax, 1], [self.wxmin, self.wymax, 1]]
        self.normalized_coordinates = [[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]

    def change_offset(self, x, y):
        self.wxmin += x
        self.wymin += y
        self.wxmax += x
        self.wymax += y
        self.update_center()

    def get_normalized_matrix(self):
        return create_normalized_matrix(self.center, self.angle_offset, self.scale)

    def update_coordinates(self):
        self.coordinates = [[self.wxmin, self.wymin, 1], [self.wxmax, self.wxmin, 1], [self.wxmax, self.wymax, 1], [self.wxmin, self.wymax, 1]]

    def change_zoom(self, min, max):
        self.wxmin += min
        self.wymin += min
        self.wxmax += max
        self.wymax += max
        self.update_coordinates()
        self.update_scale()

    def update_center(self):
        self.update_sizes()
        self.center = [(self.wxmin + self.wxmax) / 2, (self.wymin + self.wymax) / 2]

    def update_sizes(self):
        self.sizex = self.wxmax - self.wxmin
        self.sizey = self.wymax - self.wymin

    def update_scale(self):
        self.update_center()
        self.scale = [2/self.sizex, 2/self.sizey]

    def rotate(self, angle):
        self.angle_offset += angle
