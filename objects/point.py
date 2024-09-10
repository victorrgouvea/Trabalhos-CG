from objects.generic_object import GenericObject

class Point(GenericObject):
    
    def __init__(self, name, coordinates, color):
        super().__init__(name, 'point', coordinates, color)
    
    def draw(self, context, viewport_function):
        translated_coords = viewport_function(self.coordinates[0][0], self.coordinates[0][1])
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.arc(translated_coords[0], translated_coords[1], 2, 0, 2 * 3.14)
        context.fill()
        print(translated_coords)
        print(self.coordinates)
        print(self.color)