from generic_object import GenericObject


class Line(GenericObject):
        
    def __init__(self, name, coordinates, color):
        super().__init__(name, 'line', coordinates, color)
    
    def draw(self):
        print(f'Drawing a line at {self.get_coordinates} with color {self.get_color}')