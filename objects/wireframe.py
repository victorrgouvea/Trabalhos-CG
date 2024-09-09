from generic_object import GenericObject


class Wireframe(GenericObject):
    
    def __init__(self, name, coordinates, color):
        super().__init__(name, 'wireframe', coordinates, color)
    
    def draw(self):
        print(f'Drawing a wireframe at {self.get_coordinates} with color {self.get_color}')