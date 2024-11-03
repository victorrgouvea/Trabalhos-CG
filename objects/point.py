from objects.generic3d_object import Generic3dObject

class Point(Generic3dObject):

    def __init__(self, name, coordinates, color):
        super().__init__(name, 'point', coordinates, color)

    def draw(self, context, viewport_function):
        translated_coords = viewport_function(self.clipped_coords[0][0], self.clipped_coords[0][1])
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.arc(translated_coords[0], translated_coords[1], 2, 0, 2 * 3.14)
        context.fill()

