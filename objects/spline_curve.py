from objects.generic_object import GenericObject
import numpy as np


class SplineCurve(GenericObject):

    def __init__(self, name, coordinates, color, steps = 30):
        corrected_coordinates = self.generate_spline_coords_fwd(coordinates, steps)
        super().__init__(name, 'spline_curve', corrected_coordinates, color)

    def generate_spline_coords_fwd(self, points, steps):

        coords = []

        spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        delta = 1 / steps

        # Faz até a terceira derivada
        diff_matrix = np.matrix([[0, 0, 0, 1],
                                 [delta**3, delta**2, delta, 0],
                                 [6 * delta**3, 2 * delta**2, 0, 0],
                                 [6 * delta**3, 0, 0, 0]])

        for i, _ in enumerate(points):
            geometry_matrix_x = None
            geometry_matrix_y = None

            if i + 3 >= len(points):
                break

            geometry_matrix_x = np.matrix([[points[i][0]], [points[i + 1][0]], [points[i + 2][0]], [points[i + 3][0]]])
            geometry_matrix_y = np.matrix([[points[i][1]], [points[i + 1][1]], [points[i + 2][1]], [points[i + 3][1]]])

            coeff_matrix_x = spline_matrix * geometry_matrix_x
            coeff_matrix_y = spline_matrix * geometry_matrix_y

            initial_conditions_matrix_x = diff_matrix * coeff_matrix_x
            initial_conditions_matrix_y = diff_matrix * coeff_matrix_y

            new_x = initial_conditions_matrix_x[0, 0]
            new_y = initial_conditions_matrix_y[0, 0]

            delta_x = initial_conditions_matrix_x[1, 0]
            delta2_x = initial_conditions_matrix_x[2, 0]
            delta3_x = initial_conditions_matrix_x[3, 0]

            delta_y = initial_conditions_matrix_y[1, 0]
            delta2_y = initial_conditions_matrix_y[2, 0]
            delta3_y = initial_conditions_matrix_y[3, 0]

            coords.append([new_x, new_y, 1])

            for _ in range(steps):

                new_x += delta_x
                new_y += delta_y

                delta_x += delta2_x
                delta_y += delta2_y

                delta2_x += delta3_x
                delta2_y += delta3_y

                coords.append([new_x, new_y, 1])

        return coords

    def draw(self, context, viewport_function):
        context.new_path()
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.set_line_width(2)
        screen_lines = []
        for i in range(len(self.clipped_lines)):
            point_a = viewport_function(self.clipped_lines[i][0][0], self.clipped_lines[i][0][1])
            point_b = viewport_function(self.clipped_lines[i][1][0], self.clipped_lines[i][1][1])
            screen_lines.append([point_a, point_b])

        for line in screen_lines[:-1]:
            context.move_to(line[0][0], line[0][1])
            context.line_to(line[1][0], line[1][1])
            context.stroke()

        context.close_path()
