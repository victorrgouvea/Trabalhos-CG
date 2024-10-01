from objects.generic_object import GenericObject


class Line(GenericObject):

    def __init__(self, name, coordinates, color):
        super().__init__(name, 'line', coordinates, color)

    def draw(self, context, viewport_function):
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.set_line_width(2)
        begining_translated_coords = viewport_function(self.clipped_coords[0][0], self.clipped_coords[0][1])
        ending_translated_coords = viewport_function(self.clipped_coords[1][0], self.clipped_coords[1][1])
        context.move_to(begining_translated_coords[0], begining_translated_coords[1])
        context.line_to(ending_translated_coords[0], ending_translated_coords[1])
        context.stroke()
