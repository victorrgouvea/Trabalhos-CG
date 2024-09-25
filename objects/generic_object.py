from abc import ABC, abstractmethod
import numpy as np
from system.utils import create_translation_matrix, create_scale_matrix, create_rotation_matrix
class GenericObject(ABC):

    def __init__(self, name, type, coordinates, color = (0, 0, 0)):
        self.name = name
        self.type = type
        self.coordinates = []
        self.normalized_coordinates = []
        for x in coordinates:
            self.coordinates.append([x[0], x[1], 1])
        self.color = color
        self.center = self.get_center()

    @abstractmethod
    def draw(self, context, viewport_function, normalize_matrix):
        pass

    def get_center(self):
        total_x = 0
        total_y = 0

        for x in self.coordinates:
            total_x += x[0]
            total_y += x[1]

        self.center = [total_x / len(self.coordinates), total_y / len(self.coordinates)]

        return self.center

    def translate(self, dx, dy):
        return self.create_translation_matrix(dx, dy)

    def scale(self, sx, sy):
        scale_matrix = create_scale_matrix(sx, sy)
        center = self.get_center()
        translation_matrix_origin = create_translation_matrix(-center[0], -center[1])
        translation_matrix_return = create_translation_matrix(center[0], center[1])
        scale_matrix = np.matmul(translation_matrix_origin, scale_matrix)
        scale_matrix = np.matmul(scale_matrix, translation_matrix_return)
        return scale_matrix

    def rotate(self, angle, center):
        rotation_matrix = create_rotation_matrix(angle)
        translation_matrix_origin = create_translation_matrix(-center[0], -center[1])
        translation_matrix_return = create_translation_matrix(center[0], center[1])
        rotation_matrix = np.matmul(translation_matrix_origin, rotation_matrix)
        rotation_matrix = np.matmul(rotation_matrix, translation_matrix_return)
        return rotation_matrix

    def get_transformation_matrix(self, transformation):
        if transformation[0] == "T":
            return self.translate(transformation[1], transformation[2])
        elif transformation[0] == "S":
            return self.scale(transformation[1], transformation[2])
        elif transformation[0] == "R":
            if transformation[2] == "world":
                center = [0, 0]
            elif transformation[2] == "object":
                center = self.get_center()
            elif transformation[2] == "arbitrary":
                center = transformation[3]
            return self.rotate(transformation[1], center)

    def transform(self, transformations):
        transformation_matrix = self.get_transformation_matrix(transformations[0])
        for i in range(1, len(transformations)):
            transformation_matrix = np.matmul(transformation_matrix, self.get_transformation_matrix(transformations[i]))

        for x in self.coordinates:
            point = np.matrix(x)
            new_point = np.matmul(point, transformation_matrix)
            x[0] = new_point.item(0)
            x[1] = new_point.item(1)

    def apply_normalization(self, normalization_matrix):
        self.normalized_coordinates = []
        for x in self.coordinates:
            point = np.matrix(x)
            new_point = np.matmul(point, normalization_matrix)
            self.normalized_coordinates.append([new_point.item(0), new_point.item(1), 1])
