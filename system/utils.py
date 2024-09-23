import numpy as np


def create_translation_matrix(dx, dy):
    return np.matrix([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

def create_scale_matrix(sx, sy):
    return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def create_rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

def create_normalized_matrix(center, angle, scale):
    translation_matrix = create_translation_matrix(center[0], center[1])
    rotation_matrix = create_rotation_matrix(-angle)
    scale_matrix = create_scale_matrix(scale[0], scale[1])
    normalized_matrix = np.matmul(translation_matrix, rotation_matrix)
    normalized_matrix = np.matmul(normalized_matrix, scale_matrix)
    return normalized_matrix
