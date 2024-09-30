from objects.generic_object import GenericObject


class Wireframe(GenericObject):

    def __init__(self, name, coordinates, color, fill):
        super().__init__(name, 'wireframe', coordinates, color)
        self.fill = fill

    def draw(self, context, viewport_function):

        context.set_source_rgb(self.color[0], self.color[1], self.color[2])

        begining_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.move_to(begining_translated_coords[0], begining_translated_coords[1])

        for i in range(1, len(self.coordinates)):
            next_translated_coords = viewport_function(self.normalized_coordinates[i][0], self.normalized_coordinates[i][1])
            context.line_to(next_translated_coords[0], next_translated_coords[1])

        next_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.line_to(next_translated_coords[0], next_translated_coords[1])

        if self.fill:
            context.fill_preserve()
        context.set_line_width(2)
        context.stroke()


'''
from objects.generic_object import GenericObject


class Wireframe(GenericObject):

    def __init__(self, name, coordinates, color, fill):
        super().__init__(name, 'wireframe', coordinates, color)
        self.fill = fill

    def draw(self, context, viewport_function):

        context.set_source_rgb(self.color[0], self.color[1], self.color[2])

        begining_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.move_to(begining_translated_coords[0], begining_translated_coords[1])

        for i in range(1, len(self.coordinates)):
            next_translated_coords = viewport_function(self.normalized_coordinates[i][0], self.normalized_coordinates[i][1])
            context.line_to(next_translated_coords[0], next_translated_coords[1])

        next_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.line_to(next_translated_coords[0], next_translated_coords[1])

        if self.fill:
            context.fill_preserve()
        context.set_line_width(2)
        context.stroke()
'''