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

def clip_point(object_):
    clipped_lines = []
    coords = object_.normalized_coordinates
    if (-1 <= coords[0][0] <= 1) and (-1 <= coords[0][1] <= 1):
        clipped_lines.append(object_.normalized_coordinates[0])
    return clipped_lines

def clip(object_, algorithm = 'cohen-sutherland'):
        object_.clipped_coords = []
        if object_.type == 'wireframe':
            object_.clipped_coords = sutherland_hodgeman(object_)
        elif object_.type == 'point':
            object_.clipped_coords = clip_point(object_)
        else:
            if algorithm == 'cohen-sutherland':
                object_.clipped_coords = cohen_sutherland(object_)
            else:
                object_.clipped_coords = liang_barsky(object_)
        print(object_.clipped_coords)

def sutherland_hodgeman(object_):
        clipped_lines = []
        original_coords = object_.normalized_coordinates
        clipped_lines_temp = []

        for inter in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']:
            for v in range(len(original_coords)):
                line = [original_coords[v], original_coords[v + 1] if v < len(original_coords) - 1 else original_coords[0]]
                comp_inside = None
                comp_a = None
                comp_b = None
                print("teste", clipped_lines)
                print("teste2", clipped_lines_temp)
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
                    intersec = intersection(line, [inter])
                    clipped_lines_temp.append(intersec)
                elif comp_b:
                    intersec = intersection(line, [inter])
                    clipped_lines_temp.append(intersec)

            if object_.fill:
                for i, _ in enumerate(clipped_lines_temp):
                    if i < len(clipped_lines_temp) - 1:
                        if clipped_lines_temp[i][1] != clipped_lines_temp[i + 1][0]:
                            clipped_lines_temp.insert(i + 1,
                                                        [clipped_lines_temp[i][1], clipped_lines_temp[i + 1][0]])
                    else:
                        if clipped_lines_temp[i][1] != clipped_lines_temp[0][0]:
                            clipped_lines_temp.append([clipped_lines_temp[i][1], clipped_lines_temp[0][0]])

            print("teste3", clipped_lines)
            print("teste4", clipped_lines_temp)
            clipped_lines = clipped_lines_temp.copy()
            clipped_lines_temp.clear()

        return clipped_lines

def cohen_sutherland(object_):
    clipped_line = []
    region_codes = []
    line = object_.normalized_coordinates
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

    print('new line'    , new_line)
    return new_line if len(new_line) == 2 else []


def liang_barsky(object_):
    line = object_.normalized_coordinates
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
