from abc import ABC, abstractmethod
import numpy as np


class GenericObject(ABC):

    def __init__(self, name, type, coordinates, color = (0, 0, 0)):
        self.name = name
        self.type = type
        self.coordinates = []
        for x in coordinates:
            self.coordinates.append([x[0], x[1], 1])
        self.coordinates = coordinates
        self.color = color
        self.center = self.get_center()

    @abstractmethod
    def draw(self, context, viewport_functionf):
        pass

    def get_center(self):
        total_x = 0
        total_y = 0

        for x in self.coordinates:
            total_x += x[0]
            total_y += x[1]

        return (total_x / len(self.coordinates), total_y / len(self.coordinates))

    def create_translation_matrix(self, dx, dy):
        return np.matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

    def create_scale_matrix(self, sx, sy):
        return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def create_rotation_matrix(self, angle):
        return np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

    def translate(self, dx, dy):
        return self.create_translation_matrix(dx, dy)

    def scale(self, sx, sy):
        scale_matrix = self.create_scale_matrix(sx, sy)
        translation_matrix_origin = self.create_translation_matrix(-self.center[0], -self.center[1])
        translation_matrix_return = self.create_translation_matrix(self.center[0], self.center[1])
        scale_matrix = np.dot(translation_matrix_origin, scale_matrix)
        scale_matrix = np.dot(scale_matrix, translation_matrix_return)
        return scale_matrix

    def rotate(self, angle, center):
        rotation_matrix = self.create_rotation_matrix(angle)
        translation_matrix_origin = self.create_translation_matrix(-center[0], -center[1])
        translation_matrix_return = self.create_translation_matrix(center[0], center[1])
        rotation_matrix = np.dot(translation_matrix_origin, rotation_matrix)
        rotation_matrix = np.dot(rotation_matrix, translation_matrix_return)
        return rotation_matrix

    def get_transformation_matrix(self, transformation):
        if transformation[0] == "T":
            return self.translate(transformation[1], transformation[2])
        elif transformation[0] == "S":
            return self.scale(transformation[1], transformation[2])
        elif transformation[0] == "R":
            return self.rotate(transformation[1])

    def transform(self, transformations):
        transformation_matrix = self.get_transformation_matrix(transformations[0])

        for i in range(1, len(transformations)):
            transformation_matrix = np.dot(transformation_matrix, self.get_transformation_matrix(transformations[i]))

        for x in self.coordinates:
            point = np.matrix(x)
            new_point = np.dot(point, transformation_matrix)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)
