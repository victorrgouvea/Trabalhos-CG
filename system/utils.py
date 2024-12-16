import numpy as np
from math import cos, radians, sin, degrees, inf

def create_translation_matrix(dx, dy):
    return np.matrix([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

def create_scale_matrix(sx, sy):
    return np.matrix([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

def create_rotation_matrix(angle):
    angle = np.deg2rad(angle)
    return np.matrix([[np.cos(angle), -np.sin(angle), 0],
                       [np.sin(angle), np.cos(angle), 0], 
                       [0, 0, 1]])

def clip_point(object_):
    clipped_lines = []
    coords = object_.normalized_coordinates
    if (-1 <= coords[0][0] <= 1) and (-1 <= coords[0][1] <= 1):
        clipped_lines.append(object_.normalized_coordinates[0])
    return clipped_lines

def clip(object_, algorithm = 'cohen-sutherland'):
        object_.clipped_coords = []
        if object_.type == 'wireframe' and object_.fill:
            object_.clipped_lines = sutherland_hodgeman(object_)
        elif object_.type == 'point':
            object_.clipped_coords = clip_point(object_)
        elif object_.type == 'line':
            if algorithm == 'cohen-sutherland':
                object_.clipped_coords = cohen_sutherland(object_.normalized_coordinates)
            else:
                object_.clipped_coords = liang_barsky(object_.normalized_coordinates)
        else:
            object_.clipped_lines = clip_lines(object_, algorithm)

def clip_lines(object_, algorithm):
        clipped_lines = []
        normalized_lines = []
        points = object_.normalized_coordinates
        for x in range(len(points)):
            normalized_lines.append([points[x], points[x + 1] if x < len(points) - 1 else points[0]])
        for line in normalized_lines:
            if algorithm == 'cohen-sutherland':
                clipped_line = cohen_sutherland(line)
            else:
                clipped_line = liang_barsky(line)
            if len(clipped_line) > 0:
                clipped_lines.append(clipped_line)
        return clipped_lines

def sutherland_hodgeman(object_):
        points = object_.normalized_coordinates
        clipped_lines_temp = []
        clipped_lines = []
        for x in range(len(points)):
            clipped_lines.append([points[x], points[x + 1] if x < len(points) - 1 else points[0]])
        for inter in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']:
            for v in range(len(clipped_lines)):
                line = clipped_lines[v]
                comp_inside = None
                comp_a = None
                comp_b = None
                match inter:
                    case 'LEFT':
                        comp_inside = line[0][0] > -1 and line[1][0] > -1
                        comp_a = line[0][0] > -1
                        comp_b = line[1][0] > -1
                    case 'RIGHT':
                        comp_inside = line[0][0] < 1 and line[1][0] < 1
                        comp_a = line[0][0] < 1
                        comp_b = line[1][0] < 1
                    case 'BOTTOM':
                        comp_inside = line[0][1] > -1 and line[1][1] > -1
                        comp_a = line[0][1] > -1
                        comp_b = line[1][1] > -1
                    case 'TOP':
                        comp_inside = line[0][1] < 1 and line[1][1] < 1
                        comp_a = line[0][1] < 1
                        comp_b = line[1][1] < 1

                if comp_inside:
                    clipped_lines_temp.append(line)
                elif comp_a:
                    intersec = intersection(line, [['inside'], [inter]], False)
                    if intersec != []:
                        clipped_lines_temp.append(intersec)
                elif comp_b:
                    intersec = intersection(line, [[inter], ['inside']], False)
                    if intersec != []:
                        clipped_lines_temp.append(intersec)
            
            for i, _ in enumerate(clipped_lines_temp):
                if i < len(clipped_lines_temp) - 1:
                    if clipped_lines_temp[i][1] != clipped_lines_temp[i + 1][0]:
                        clipped_lines_temp.insert(i + 1,
                                                    [clipped_lines_temp[i][1], clipped_lines_temp[i + 1][0]])
                else:
                    if clipped_lines_temp[i][1] != clipped_lines_temp[0][0]:
                        clipped_lines_temp.append([clipped_lines_temp[i][1], clipped_lines_temp[0][0]])
            
            clipped_lines = clipped_lines_temp.copy()
            clipped_lines_temp.clear()
        return clipped_lines

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

def intersection(line, intersections, condition = True):

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

            if (new_x < -1 or new_x > 1) or (new_y < -1 or new_y > 1) and condition:
                if diagonal:
                    continue
                else:
                    return []

            new_line.append([new_x, new_y])
            break

    return new_line if len(new_line) == 2 else []

def liang_barsky(line):
    p1 = -(line[1][0] - line[0][0])
    p2 = -p1
    p3 = -(line[1][1] - line[0][1])
    p4 = -p3

    q1 = line[0][0] - (-1)
    q2 = 1 - line[0][0]
    q3 = line[0][1] - (-1)
    q4 = 1 - line[0][1]

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

    new_vector_a = [line[0][0] + p2 * max_negative, line[0][1] + p4 * max_negative]
    new_vector_b = [line[0][0] + p2 * min_positive, line[0][1] + p4 * min_positive]

    return [new_vector_a, new_vector_b]

def create_translation_matrix_3d(direction):
    return np.matrix([[1.0, 0.0, 0.0, 0],
                        [0.0, 1.0, 0.0, 0],
                        [0.0, 0.0, 1.0, 0],
                        [direction[0], direction[1], direction[2], 1.0]])
    
def create_rotation_matrix_3d(angle, inverse: bool = False) -> np.matrix:
    sinx = sin(radians(angle[0]))
    cosx = cos(radians(angle[0]))
    siny = sin(radians(angle[1]))
    cosy = cos(radians(angle[1]))
    sinz = sin(radians(angle[2]))
    cosz = cos(radians(angle[2]))

    rotation_x = np.matrix([[1.0, 0.0, 0.0, 0.0],
                            [0.0, cosx, -sinx, 0.0],
                            [0.0, sinx, cosx, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])

    rotation_y = np.matrix([[cosy, 0.0, siny, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [-siny, 0.0, cosy, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])

    rotation_z = np.matrix([[cosz, -sinz, 0.0, 0.0],
                            [sinz, cosz, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])

    if inverse:
        return rotation_x @ rotation_y @ rotation_z

    return rotation_z @ rotation_y @ rotation_x

def create_scale_matrix_3d(scale):

    return np.matrix([[scale[0], 0.0, 0.0, 0.0],
                        [0.0, scale[1], 0.0, 0.0],
                        [0.0, 0.0, scale[2], 0.0],
                        [0.0, 0.0, 0.0, 1.0]])


def build_perspective_matrix(cop_distance: float) -> np.matrix:
    '''
    Constrói a matriz de perspectiva.
    '''
    return np.matrix([[1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 1.0 / cop_distance, 0.0]])

def normalize_homogeneous_coordinates(point):
    '''
    Normaliza coordenadas homogêneas para coordenadas cartesianas.
    '''
    point = np.array(point).flatten()
    if point[3] != 0:
        return [point[0] / point[3], point[1] / point[3], point[2] / point[3]]
    return [point[0], point[1], point[2]]  # Caso w == 0

def normalize_vector(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


def create_projection_matrix_3d(cop, normal):
    translation = create_translation_matrix_3d([-cop[0], -cop[1], -cop[2]])
    normal_shadow_xz = [normal[0], 0.0, normal[2]]

    rotation_y = degrees(np.matmul([0.0, 0.0, 1.0], normal_shadow_xz))

    if normal[0] > 0.0:
        rotation_y = 360 - rotation_y

    normal_rotation_matrix = create_rotation_matrix_3d([0.0, rotation_y, 0.0])
    new_normal = np.matmul(normal_rotation_matrix, [normal[0], normal[1], normal[2], 1])
    normal = [new_normal[0, 0], new_normal[0, 1], new_normal[0, 2]]

    rotation_x = degrees(np.matmul([0.0, 0.0, 1.0], normal))

    if normal[2] < 0.0:
        rotation_x = 360 - rotation_x

    rotation_x = create_rotation_matrix_3d([rotation_x, 0.0, 0.0])
    rotation_y = create_rotation_matrix_3d([0.0, rotation_y, 0.0])

    return rotation_x @ rotation_y @ translation

def create_normalized_matrix(center, angle, scale, cop = 0, normal = (0,0,0), ignore_projection = False):
    translation_matrix = create_translation_matrix_3d(center)
    rotation_matrix = create_rotation_matrix_3d([-angle[0], -angle[1], -angle[2]])
    scale_matrix = create_scale_matrix_3d(scale)
    normalized_matrix = np.matmul(translation_matrix, rotation_matrix)
    normalized_matrix = np.matmul(normalized_matrix, scale_matrix)
    if (not ignore_projection):
        normalized_matrix = np.matmul(create_projection_matrix_3d(cop, normal), normalized_matrix)
    return normalized_matrix

def angle_between_vectors(vector1, vector2):
        a =  np.dot(vector1, vector2)
        b = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return np.degrees(np.arccos(a / b))

def get_axis_rotation(point, rotation_angle, axis):
        x = point[0]
        y = point[1]
        z = point[2]

        x_axis = np.matrix([1, 0, 0])
        x_angle = angle_between_vectors(x_axis, axis)
        z_axis = np.matrix([0, 0, 1])
        z_angle = angle_between_vectors(z_axis, axis)
        trans = create_translation_matrix_3d([-x, -y, -z])
        rot_x = create_rotation_matrix_3d([-x_angle, 0, 0])
        rot_z = create_rotation_matrix_3d([0, 0, -z_angle])
        rotation = create_rotation_matrix_3d([0, rotation_angle, 0])
        rev_rot_x = create_rotation_matrix_3d([x_angle, 0, 0])
        rev_rot_z = create_rotation_matrix_3d([0, 0, z_angle])
        reverse_trans = create_translation_matrix_3d(point)

        return trans @ rot_x @ rot_z @ rotation @ rev_rot_z @ rev_rot_x @ reverse_trans