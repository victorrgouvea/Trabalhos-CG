from abc import ABC, abstractmethod

class GenericObject(ABC):

    def __init__(self, name, type, coordinates, color = (0, 0, 0)):
        self.name = name
        self.type = type
        self.coordinates = []
        for x in coordinates:
            self.coordinates.append(x)
        self.coordinates = coordinates
        self.color = color
    
    @abstractmethod
    def draw(self, context, viewport_functionf):
        pass
