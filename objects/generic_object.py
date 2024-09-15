from abc import ABC, abstractmethod

class GenericObject(ABC):

    def __init__(self, name, type, coordinates, color = (0, 0, 0)):
        self.name = name
        self.type = type
        self.coordinates = []
        for x in coordinates:
            self.coordinates.append([x[0], x[1], 1])
        self.coordinates = coordinates
        self.color = color
        self.center = self.get_center()

    @abstractmethod
    def draw(self, context, viewport_functionf):
        pass

    def get_center(self):
        total_x = 0
        total_y = 0

        for x in self.coordinates:
            total_x += x[0]
            total_y += x[1]

        return (total_x / len(self.coordinates), total_y / len(self.coordinates))
