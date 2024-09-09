from abc import ABC, abstractmethod

class GenericObject(ABC):

    def __init__(self, name, type, coordinates, color):
        self.__name = name
        self.__type = type
        self.__coordinates = coordinates
        self.__color = color

    @property
    def get_coordinates(self):
        return self.__coordinates
    
    @property
    def get_color(self):
        return self.__color

    @property
    def get_name(self):
        return self.__name
    
    @property
    def get_type(self):
        return self.__type
    
    @abstractmethod
    def draw(self):
        pass
