from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe
from system.utils import clip

class DisplayFile:
    def __init__(self, view_port):
        self.objects = []
        self.view_port = view_port
        self.window = view_port.window

    def add_object(self, name, type, coords, color, fill = False):
        if type == 'line':
            object = Line(name, coords, color)
        elif type == 'point':
            object = Point(name, coords, color)
        elif type == 'wireframe':
            object = Wireframe(name, coords, color, fill)

        self.objects.append(object)

        return object

    def draw(self, context):
        # We pass the function as an arg in case we want to make a switch case later
        norm_matrix = self.window.get_normalized_matrix()
        for objects in self.objects:
             objects.apply_normalization(norm_matrix)
             clip(objects)
             if objects.clipped_coords:
                objects.draw(context, self.view_port.transform)
