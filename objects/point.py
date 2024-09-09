from generic_object import GenericObject

class Point(GenericObject):
    
    def __init__(self, name, coordinates, color):
        super().__init__(name, 'point', coordinates, color)
    
    def draw(self):
        print(f'Drawing a point at {self.get_coordinates} with color {self.get_color}')