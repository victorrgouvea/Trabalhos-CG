import numpy as np
from objects.generic3d_object import Generic3dObject

class BSplineSurface(Generic3dObject):
    def __init__(self, name, control_points, drawing_step=6) -> None:
        self._drawing_step = drawing_step
        surface_curves = self.compute_surface_curves(control_points)
        points, lines_indexes = self.curves_to_graphic_obj(surface_curves)
        super().__init__(name, 'surface', points)

    def compute_surface_curves(self, control_points):
        # Matriz da B-Spline cúbica
        b_spline_matrix = (1 / 6) * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        delta = 1 / self._drawing_step
        # Matriz de diferenças forward -> S e T tem o mesmo passo, então são iguais
        diff_matrix = np.array(
            [
                [0, 0, 0, 1],
                [delta ** 3, delta ** 2, delta, 0],
                [6 * delta ** 3, 2 * delta ** 2, 0, 0],
                [6 * delta ** 3, 0, 0, 0],
            ]
        )
        curves = []
        # Para cada bloco de 4x4 pontos de controle, computa a superfície
        for i in range(len(control_points) - 3):
            for j in range(len(control_points[i]) - 3):
                # Extrai os pontos de controle para o patch atual
                g_matrix_x = np.array([[control_points[i + m][j + n].x for n in range(4)] for m in range(4)])
                g_matrix_y = np.array([[control_points[i + m][j + n].y for n in range(4)] for m in range(4)])
                g_matrix_z = np.array([[control_points[i + m][j + n].z for n in range(4)] for m in range(4)])

                # Calcula os coeficientes da superfície
                coeff_matrix_x = b_spline_matrix @ g_matrix_x @ b_spline_matrix.T
                coeff_matrix_y = b_spline_matrix @ g_matrix_y @ b_spline_matrix.T
                coeff_matrix_z = b_spline_matrix @ g_matrix_z @ b_spline_matrix.T

                # Matriz de condições iniciais para a direção s
                dd_matrix_x = diff_matrix @ coeff_matrix_x @ diff_matrix.T
                dd_matrix_y = diff_matrix @ coeff_matrix_y @ diff_matrix.T
                dd_matrix_z = diff_matrix @ coeff_matrix_z @ diff_matrix.T

                curves_s = self.draw_curves_in_one_direction(dd_matrix_x, dd_matrix_y, dd_matrix_z)
                curves.extend(curves_s)

                # Para outra direção (transposta)
                dd_matrix_x = (diff_matrix @ coeff_matrix_x @ diff_matrix.T).T
                dd_matrix_y = (diff_matrix @ coeff_matrix_y @ diff_matrix.T).T
                dd_matrix_z = (diff_matrix @ coeff_matrix_z @ diff_matrix.T).T

                curves_t = self.draw_curves_in_one_direction(dd_matrix_x, dd_matrix_y, dd_matrix_z)
                curves.extend(curves_t)

        return curves

    def update_dd_matrix(self, DD_x, DD_y, DD_z):
        for i in range(3):
            for j in range(4):
                DD_x[i][j] += DD_x[i + 1][j]
                DD_y[i][j] += DD_y[i + 1][j]
                DD_z[i][j] += DD_z[i + 1][j]
        return DD_x, DD_y, DD_z

    def draw_curves_in_one_direction(self, dd_matrix_x, dd_matrix_y, dd_matrix_z):
        curves = []
        for _ in range(self._drawing_step):
            curve = self.draw_curve_foward_differences(
                dd_matrix_x[0][0], dd_matrix_x[0][1], dd_matrix_x[0][2], dd_matrix_x[0][3],
                dd_matrix_y[0][0], dd_matrix_y[0][1], dd_matrix_y[0][2], dd_matrix_y[0][3],
                dd_matrix_z[0][0], dd_matrix_z[0][1], dd_matrix_z[0][2], dd_matrix_z[0][3]
            )
            curves.append(curve)
            dd_matrix_x, dd_matrix_y, dd_matrix_z = self.update_dd_matrix(dd_matrix_x, dd_matrix_y, dd_matrix_z)

        # Última curva necessária
        curve = self.draw_curve_foward_differences(
            dd_matrix_x[0][0], dd_matrix_x[0][1], dd_matrix_x[0][2], dd_matrix_x[0][3],
            dd_matrix_y[0][0], dd_matrix_y[0][1], dd_matrix_y[0][2], dd_matrix_y[0][3],
            dd_matrix_z[0][0], dd_matrix_z[0][1], dd_matrix_z[0][2], dd_matrix_z[0][3]
        )
        curves.append(curve)
        return curves

    # DesenhaCurvaFwdDiff( n, x, Dx, D2x, D3x, y, Dy,D2y, D3y, z, Dz, D2z, D3z)
    # Mesmo algoritmo utilizado em BSplineCurve
    def draw_curve_foward_differences(self, x, delta_x, delta2_x, delta3_x,
                                      y, delta_y, delta2_y, delta3_y,
                                      z, delta_z, delta2_z, delta3_z):
        curve_points = [Point(x, y, z)]
        for _ in range(self._drawing_step):
            x += delta_x
            y += delta_y
            z += delta_z
            delta_x += delta2_x
            delta_y += delta2_y
            delta_z += delta2_z
            delta2_x += delta3_x
            delta2_y += delta3_y
            delta2_z += delta3_z
            curve_points.append(Point(x, y, z))
        return curve_points

    def curves_to_graphic_obj(self, curves):
        points = []
        lines_indexes = []
        point_to_index = {}
        for curve in curves:
            line_indexes = []
            for point in curve:
                if point not in point_to_index:
                    point_to_index[point] = len(points)
                    points.append(point)
                line_indexes.append(point_to_index[point])
            lines_indexes.append(line_indexes)
        return points, lines_indexes

    def draw(self, context, viewport_transform, window_min, window_max, clipping):

      for i in self._point_indexes:
          self._draw_point(
              context, i, viewport_transform, window_min, window_max, clipping
          )

      for line in self._lines_indexes:
          self._draw_line(
              context, line, viewport_transform, window_min, window_max, clipping
          )

    def draw_line(self, context, point1, point2):
        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(point1[0], point1[1])
        context.line_to(point2[0], point2[1])
        context.stroke()


    def _draw_point(self, context, index, viewport_transform, window_min, window_max, clipping):
      point = self._normalized_points[index]
      if (not point.ignore) and clipping.clip_point(window_max, window_min, point):
          new_point = viewport_transform(point)
          self.draw_line(context, new_point, [new_point[0] + 1, new_point[1] + 1] )

    def _draw_line(self, context, line_indexes, viewport_transform, window_min, window_max, clipping):
        last_index, *others = line_indexes
        for i in others:
            point1 = self.normalized_points[last_index]
            point2 = self.normalized_points[i]
            last_index = i

            if point1.ignore and point2.ignore:
                continue

            new_line = clipping.clip_line(window_max, window_min, point1, point2)
            if new_line:
                initial_point = viewport_transform(new_line[0])
                end_point = viewport_transform(new_line[1])
                super().draw_line(context, initial_point, end_point)
