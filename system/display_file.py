from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe


class DisplayFile:
    def __init__(self):
        self.objects = []

    def add_object(self, name, type, coords):
        color = (0, 0, 0)
        if type == 'line':
            object = Line(name, coords, color)
        elif type == 'point':
            object = Point(name, coords, color)
        elif type == 'wireframe':
            object = Wireframe(name, coords, color)

        self.objects.append(object)

    def update_draw(self, context):
        # for object in self.objects:
        #     object.draw(context, )
        pass