from objects.generic_object import GenericObject
import numpy as np

class BezierCurve(GenericObject):

    def __init__(self, name, coordinates, color, steps = 100):
        corrected_coordinates = []

        for i in range(0, len(coordinates), 3):
            if i == len(coordinates) - 1:
                break

            corrected_coordinates += self.generate_curve_coords([coordinates[i],
                                                       coordinates[i + 1],
                                                       coordinates[i + 2],
                                                       coordinates[i + 3],
                                                       ], steps)

        super().__init__(name, 'bezier_curve', coordinates, color)

    def generate_curve_coords(self, coords, steps):

        bezier_points_x = np.matrix([[coords[0][0]], [coords[1][0]], [coords[2][0]], [coords[3][0]]])
        bezier_points_y = np.matrix([[coords[0][1]], [coords[1][1]], [coords[2][1]], [coords[3][1]]])

        bezier_matrix = np.matrix([[-1, 3, -3, 1],
                                   [3, -6, 3, 0],
                                   [-3, 3, 0, 0],
                                   [1, 0, 0, 0]])

        coordinates = []

        for step in range(steps):

            t = step / steps

            step_matrix = np.matrix([t**3, t**2, t, 1])

            new_x = step_matrix * bezier_matrix * bezier_points_x
            new_y = step_matrix * bezier_matrix * bezier_points_y

            coordinates.append([new_x[0, 0], new_y[0, 0], 1])

        return coordinates

    def draw(self, context, viewport_function):
        context.new_path()
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.set_line_width(2)
        screen_lines = []
        for i in range(len(self.clipped_lines)):
            point_a = viewport_function(self.clipped_lines[i][0][0], self.clipped_lines[i][0][1])
            point_b = viewport_function(self.clipped_lines[i][1][0], self.clipped_lines[i][1][1])
            screen_lines.append([point_a, point_b])

        if self.fill and len(screen_lines) > 0:
                context.move_to(screen_lines[0][0][0], screen_lines[0][0][1])

        for line in screen_lines:
            if self.fill:
                context.line_to(line[1][0], line[1][1])
            else:
                context.move_to(line[0][0], line[0][1])
                context.line_to(line[1][0], line[1][1])
                context.stroke()

        context.close_path()

        if self.fill:
            context.fill()
