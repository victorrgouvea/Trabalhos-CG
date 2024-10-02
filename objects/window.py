import numpy as np
from system.utils import create_normalized_matrix, create_rotation_matrix, create_translation_matrix, create_scale_matrix
from objects.border import Border

class Window():

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
        self.coordinates = [[self.wxmin, self.wymin, 1],
                            [self.wxmax, self.wxmin, 1],
                            [self.wxmax, self.wymax, 1],
                            [self.wxmin, self.wymax, 1]]
        self.normalized_coordinates = [[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]
        self.border = Border(self.coordinates)

    def change_offset(self, x, y):
        point = np.matrix([x, y, 1])
        rot_mat = create_rotation_matrix(self.angle_offset)
        point = np.matmul(point, rot_mat)
        translation_mat = create_translation_matrix(point.item(0), point.item(1))
        for x in self.coordinates:
            point = np.matrix(x)
            new_point = np.matmul(point, translation_mat)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)
        self.update_min_max()
        self.update_center()

    def get_normalized_matrix(self):
        return create_normalized_matrix(self.center, self.angle_offset, self.scale)

    def update_min_max(self):
        self.wxmin = self.coordinates[0][0]
        self.wymin = self.coordinates[0][1]
        self.wxmax = self.coordinates[2][0]
        self.wymax = self.coordinates[2][1]

    def update_coordinates(self):
        self.coordinates = [[self.wxmin, self.wymin, 1], [self.wxmax, self.wxmin, 1], [self.wxmax, self.wymax, 1], [self.wxmin, self.wymax, 1]]

    def change_zoom(self, sx, sy):
        scale_matrix = create_scale_matrix(sx, sy)
        translation_matrix_origin = create_translation_matrix(-self.center[0], -self.center[1])
        translation_matrix_return = create_translation_matrix(self.center[0], self.center[1])
        scale_matrix = np.matmul(translation_matrix_origin, scale_matrix)
        scale_matrix = np.matmul(scale_matrix, translation_matrix_return)
        for x in self.coordinates:
            point = np.matrix(x)
            new_point = np.matmul(point, scale_matrix)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)
        self.update_min_max()
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
