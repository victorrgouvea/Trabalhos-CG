from abc import ABC, abstractmethod
import numpy as np
from system.utils import create_translation_matrix_3d, create_scale_matrix_3d, create_rotation_matrix_3d, get_axis_rotation, normalize_homogeneous_coordinates
class Generic3dObject(ABC):

    def __init__(self, name, type, coordinates, color = (0, 0, 0), fill = False):
        self.name = name
        self.type = type
        self.coordinates = []
        self.normalized_coordinates = []
        self.clipped_coords = []
        self.fill = fill
        self.is3d = False
        lastUsedCoord = coordinates[0]
        for x in coordinates:
            if (len(x) == 2):
                self.coordinates.append([x[0], x[1], 0])
            else:
                self.coordinates.append([x[0], x[1], x[2]])

            if ((len(x) == 3) and (lastUsedCoord[2] != x[2])):
                self.is3d = True
        self.color = color
        self.center = self.get_center()
        self.clipped_lines = []

    @abstractmethod
    def draw(self, context, viewport_function, normalize_matrix):
        pass

    def get_center(self):
        total_x = 0
        total_y = 0
        total_z = 0

        for x in self.coordinates:
            total_x += x[0]
            total_y += x[1]
            total_z += x[2]

        self.center = [total_x / len(self.coordinates), total_y / len(self.coordinates), total_z / len(self.coordinates)]

        return self.center

    def translate(self, vector, angle = [0,0,0]):
        vector = [vector[0], vector[1], vector[2], 1]
        point = np.matrix(vector)
        rot_mat = create_rotation_matrix_3d(angle)
        point = np.matmul(point, rot_mat)
        return create_translation_matrix_3d([point.item(0), point.item(1), point.item(2)])

    def scale(self, vector):
        vector = [vector[0], vector[1], vector[2], 1]
        scale_matrix = create_scale_matrix_3d(vector)
        center = self.get_center()
        translation_matrix_origin = create_translation_matrix_3d([-center[0], -center[1], -center[2]])
        translation_matrix_return = create_translation_matrix_3d([center[0], center[1], center[2]])
        scale_matrix = np.matmul(translation_matrix_origin, scale_matrix)
        scale_matrix = np.matmul(scale_matrix, translation_matrix_return)
        return scale_matrix

    def rotate(self, angle, center, rot_type):
        if rot_type == "axis":
            rotation_matrix = get_axis_rotation(self.center, angle, center)
        else:
            rotation_matrix = create_rotation_matrix_3d([0, 0, angle])
            translation_matrix_origin = create_translation_matrix_3d([-center[0], -center[1], -center[2]])
            translation_matrix_return = create_translation_matrix_3d([center[0], center[1], center[2]])
            rotation_matrix = np.matmul(translation_matrix_origin, rotation_matrix)
            rotation_matrix = np.matmul(rotation_matrix, translation_matrix_return)
        return rotation_matrix


    def get_transformation_matrix(self, transformation):
        if transformation[0] == "T":
            return self.translate(transformation[1], transformation[2])
        elif transformation[0] == "S":
            return self.scale(transformation[1])
        elif transformation[0] == "R":
            if transformation[2] == "world":
                center = [0, 0, 0]
            elif transformation[2] == "object":
                center = self.get_center()
            elif transformation[2] == "arbitrary":
                center = transformation[3]
            elif transformation[2] == "axis":
                center = transformation[3]
            return self.rotate(transformation[1], center, transformation[2])

    def transform(self, transformations):
        transformation_matrix = self.get_transformation_matrix(transformations[0])
        for i in range(1, len(transformations)):
            transformation_matrix = np.matmul(transformation_matrix, self.get_transformation_matrix(transformations[i]))
        new_coords = []
        for x in self.coordinates:
            x = [x[0], x[1], x[2], 1]
            point = np.matrix(x)
            new_point = np.matmul(point, transformation_matrix)
            new_coords.append([new_point.item(0), new_point.item(1), new_point.item(2)])
        self.coordinates = new_coords

    def apply_normalization(self, normalization_matrix):
        self.normalized_coordinates = []
        for x in self.coordinates:
            x = [x[0], x[1], x[2], 1]
            point = np.matrix(x)
            new_point = np.matmul(point, normalization_matrix)
            new_point = normalize_homogeneous_coordinates(new_point)
            print(new_point)
            self.normalized_coordinates.append([new_point[0], new_point[1], new_point[2]])
