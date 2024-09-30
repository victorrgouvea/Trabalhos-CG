import numpy as np
from math import inf

def create_translation_matrix(dx, dy):
    return np.matrix([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

def create_scale_matrix(sx, sy):
    return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def create_rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.matrix([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

def create_normalized_matrix(center, angle, scale):
    translation_matrix = create_translation_matrix(-center[0], -center[1])
    rotation_matrix = create_rotation_matrix(-angle)
    scale_matrix = create_scale_matrix(scale[0], scale[1])
    normalized_matrix = np.matmul(translation_matrix, rotation_matrix)
    normalized_matrix = np.matmul(normalized_matrix, scale_matrix)
    return normalized_matrix

def cohen_sutherland(line):
    clipped_line = []
    region_codes = []

    # Get the code for each point of the line
    for point in line:
        region_code = 0b0000
        if point[0] < -1:
            region_code |= 0b0001
        if point[0] > 1:
            region_code |= 0b0010
        if point[1] < -1:
            region_code |= 0b0100
        if point[1] > 1:
            region_code |= 0b1000
        region_codes.append(region_code)

    # Line completely inside the window
    if (region_codes[0] | region_codes[1]) == 0b0000:
        clipped_line = line
    # Line partially inside the window
    elif (region_codes[0] & region_codes[1]) == 0b0000:
        intersections = []

        for region_code in region_codes:
            match region_code:
                case 0b0000:
                    intersections.append(['INSIDE'])
                case 0b0001:
                    intersections.append(['LEFT'])
                case 0b0010:
                    intersections.append(['RIGHT'])
                case 0b1000:
                    intersections.append(['TOP'])
                case 0b0100:
                    intersections.append(['BOTTOM'])
                case 0b1001:
                    intersections.append(['LEFT', 'TOP'])
                case 0b0101:
                    intersections.append(['LEFT', 'BOTTOM'])
                case 0b0110:
                    intersections.append(['RIGHT', 'BOTTOM'])
                case 0b1010:
                    intersections.append(['RIGHT', 'TOP'])

        clipped_line = intersection(line, intersections)

    return clipped_line

def intersection(line, intersections):

    m = inf

    if (line[1][0] - line[0][0]) != 0:
        m = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])

    new_line = []

    for v in range(len(intersections)):
        point = line[v]
        inter = intersections[v]
        diagonal = True if len(inter) == 2 else False
        for double_inter in inter:
            new_x = point[0]
            new_y = point[1]

            match double_inter:
                case 'LEFT':
                    new_x = -1
                    new_y = m * (-1 - point[0]) + point[1]

                case 'RIGHT':
                    new_x = 1
                    new_y = m * (1 - point[0]) + point[1]

                case 'TOP':
                    new_x = point[0] + (1.0 / m) * (1 - point[1])
                    new_y = 1

                case 'BOTTOM':
                    new_x = point[0] + (1.0 / m) * (-1 - point[1])
                    new_y = -1

            if (new_x < -1 or new_x > 1) or (new_y < -1 or new_y > 1):
                if diagonal:
                    continue
                else:
                    return []

            new_line.append([new_x, new_y])
            break

    return new_line if len(new_line) == 2 else []


def liang_barsky(window, line):
    '''
    Clipping de linha com o algoritmo de Liang-Barsky.
    '''

    p1 = -(line[1].x - line[0].x)
    p2 = -p1
    p3 = -(line[1].y - line[0].y)
    p4 = -p3

    q1 = line[0].x - window.normalized_origin.x
    q2 = window.normalized_extension.x - line[0].x
    q3 = line[0].y - window.normalized_origin.y
    q4 = window.normalized_extension.y - line[0].y

    positives = [1]
    negatives = [0]

    if (p1 == 0 and q1 < 0) or (p2 == 0 and q2 < 0) or (p3 == 0 and q3 < 0) or (p4 == 0 and q4 < 0):
        return []

    if p1 != 0:
        ratio_1 = q1 / p1
        ratio_2 = q2 / p2

        if p1 < 0:
            positives.append(ratio_2)
            negatives.append(ratio_1)
        else:
            positives.append(ratio_1)
            negatives.append(ratio_2)
    if p3 != 0:
        ratio_3 = q3 / p3
        ratio_4 = q4 / p4

        if p3 < 0:
            positives.append(ratio_4)
            negatives.append(ratio_3)
        else:
            positives.append(ratio_3)
            negatives.append(ratio_4)

    max_negative = max(negatives)
    min_positive = min(positives)

    if max_negative > min_positive:
        return []

    new_vector_a = [line[0].x + p2 * max_negative, line[0].y + p4 * max_negative]
    new_vector_b = [line[0].x + p2 * min_positive, line[0].y + p4 * min_positive]

    return [new_vector_a, new_vector_b]

# def get_intersection_point()

