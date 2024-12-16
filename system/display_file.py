from objects.line import Line
from objects.point import Point
from objects.wireframe3d import Wireframe3D
from objects.bezier_curve import BezierCurve
from objects.spline_curve import SplineCurve
from system.utils import clip

class DisplayFile:
    def __init__(self, view_port):
        self.objects = []
        self.view_port = view_port
        self.window = view_port.window
        self.clip_algorithm = 'cohen-sutherland'

    def add_object(self, name, type, coords, color, fill = False):
        if type == 'line':
            object = Line(name, coords, color)
        elif type == 'point':
            object = Point(name, coords, color)
        elif type == 'wireframe':
            object = Wireframe3D(name, coords, color, fill)
        elif type == 'bezier curve':
            object = BezierCurve(name, coords, color)
        elif type == 'spline curve':
            object = SplineCurve(name, coords, color)

        self.objects.append(object)

        return object

    def draw(self, context):
        # We pass the function as an arg in case we want to make a switch case later
        norm_matrix = self.window.get_normalized_matrix()
        border_norm_matrix = self.window.get_normalized_matrix(True)
        for objects in self.objects:
             
            if objects.is3d:
                objects.apply_normalization(norm_matrix)
            else:
                objects.apply_normalization(border_norm_matrix)

            clip(objects, self.clip_algorithm)
            if objects.clipped_coords or objects.clipped_lines:
                objects.draw(context, self.view_port.transform)

        if self.window.border.normalized_coordinates == []:
            self.window.border.apply_normalization(border_norm_matrix)
        
        self.window.border.draw(context, self.view_port.transform)
