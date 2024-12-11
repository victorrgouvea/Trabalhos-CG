import numpy as np
from objects.generic3d_object import Generic3dObject

class BezierSurface(Generic3dObject):

    '''
    Superfície.
    '''

    def __init__(self, points, steps, name, color) -> None:
        coords, _ = self.generate_surface_coords(points, steps)
        super().__init__(name, 'surface', coords, color)

    def generate_surface_coords(self, points, steps):
        '''
        Gera uma superfície.
        '''

        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        b_spline_matrix_t = b_spline_matrix.getT()

        surface_coords = []
        lines = []

        for i, _ in enumerate(points):

            geometry_matrix_x = None
            geometry_matrix_y = None
            geometry_matrix_z = None

            if i + 15 < len(points):
                geometry_matrix_x = np.matrix([[points[i+j][0] for j in range(4)] for i in range(0, len(points), 4)])
                geometry_matrix_y = np.matrix([[points[i+j][1] for j in range(4)] for i in range(0, len(points), 4)])
                geometry_matrix_z = np.matrix([[points[i+j][2] for j in range(4)] for i in range(0, len(points), 4)])
            else:
                break

            line_index = 0
            fill_curve_a = True
            curve_a = []
            curve_b = []

            for step_s in range(steps):
                s = step_s / steps
                step_matrix_s = np.matrix([s**3, s**2, s, 1])
                for step_t in range(steps):
                    t = step_t / steps
                    step_matrix_t = np.matrix([[t**3], [t**2], [t], [1]])
                    new_x = step_matrix_s * b_spline_matrix * geometry_matrix_x * b_spline_matrix_t * step_matrix_t
                    new_y = step_matrix_s * b_spline_matrix * geometry_matrix_y * b_spline_matrix_t * step_matrix_t
                    new_z = step_matrix_s * b_spline_matrix * geometry_matrix_z * b_spline_matrix_t * step_matrix_t
                    surface_coords.append([new_x[0, 0], new_y[0, 0], new_z[0, 0]])

                    if line_index + 1 < len(surface_coords):
                        lines.append((line_index, line_index + 1))

                        if fill_curve_a:
                            curve_a.append(line_index)
                        else:
                            curve_b.append(line_index)
                        line_index += 1

                if fill_curve_a:
                    curve_a.append(line_index)
                else:
                    curve_b.append(line_index)

                if len(curve_a) > 0 and len(curve_b) > 0:

                    for index_a, index_b in zip(curve_a, curve_b):
                        lines.append((index_a, index_b))

                    curve_a = curve_b.copy()
                    curve_b.clear()

                line_index += 1
                fill_curve_a = False

        return (tuple(surface_coords), tuple(lines))

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
