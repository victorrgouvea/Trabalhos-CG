import numpy as np
from system.utils import create_normalized_matrix, create_rotation_matrix_3d, create_translation_matrix_3d, create_scale_matrix_3d, create_rotation_matrix
from objects.border import Border

class Window():

    def __init__(self, wx, wy) -> None:
        self.wxmin = -wx/2
        self.wymin = -wy/2
        self.wxmax = wx/2
        self.wymax = wy/2
        self.sizex = wx
        self.sizey = wy
        self.scale = [2/self.sizex, 2/self.sizey, 1]
        self.center = [(self.wxmin + self.wxmax) / 2, (self.wymin + self.wymax) / 2, 0]
        self.angle_offset = 0
        self.coordinates = [[self.wxmin, self.wymin, 0],
                            [self.wxmin, self.wymax, 0],
                            [self.wxmax, self.wymax, 0],
                            [self.wxmax, self.wymin, 0]]
        self.border = Border(self.coordinates)
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

    def calculate_x_axis(self):
        return np.subtract(self.coords[2], self.coords[1])

    def calculate_y_vector(self):
        return np.subtract(self.coords[1] - self.coords[0])

    def calculate_z_vector(self):
        return np.cross((self.calculate_x_axis() / 2.0), (self.calculate_y_vector() / 2.0))

    def change_offset(self, x, y):
        point = np.matrix([x, y, 0, 1])
        rot_mat = create_rotation_matrix_3d([0, 0, self.angle_offset])
        point = np.matmul(point, rot_mat)
        translation_mat = create_translation_matrix_3d([point.item(0), point.item(1), point.item(2)])
        for x in self.coordinates:
            point = np.matrix([x[0], x[1], x[2], 1])
            new_point = np.matmul(point, translation_mat)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)
            x[2] = new_point.item(2)
        self.update_min_max()
        self.update_center()

    def get_normalized_matrix(self):
        return create_normalized_matrix(self.center, self.angle_offset, self.scale)

    def update_min_max(self):
        self.wxmin = self.coordinates[0][0]
        self.wymin = self.coordinates[0][1]
        self.wxmax = self.coordinates[2][0]
        self.wymax = self.coordinates[2][1]

    def change_zoom(self, sx, sy):
        scale_matrix = create_scale_matrix_3d([sx, sy, 1, 1])
        translation_matrix_origin = create_translation_matrix_3d([-self.center[0], -self.center[1], -self.center[2]])
        translation_matrix_return = create_translation_matrix_3d([self.center[0], self.center[1], self.center[2]])
        scale_matrix = np.matmul(translation_matrix_origin, scale_matrix)
        scale_matrix = np.matmul(scale_matrix, translation_matrix_return)
        for x in self.coordinates:
            point = np.matrix([x[0], x[1], x[2], 1])
            print(point, scale_matrix)
            new_point = np.matmul(point, scale_matrix)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)
        self.update_min_max()
        self.update_scale()

    def update_center(self):
        self.update_sizes()
        total = [0, 0, 0]
        for x in (self.coordinates):
            total[0] += x[0]
            total[1] += x[1]
            total[2] += x[2]
        
        self.center = [total[0] / len(self.coordinates), total[1] / len(self.coordinates), total[2] / len(self.coordinates)]

    def update_sizes(self):
        self.sizex = self.wxmax - self.wxmin
        self.sizey = self.wymax - self.wymin

    def update_scale(self):
        self.update_center()
        self.scale = [2/self.sizex, 2/self.sizey]

    def rotate(self, angle):
        self.angle_offset += angle
