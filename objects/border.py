from objects.generic3d_object import Generic3dObject


class Border(Generic3dObject):

    def __init__(self, coords):
        super().__init__('Border', 'wireframe', coords)

    def draw(self, context, viewport_function):
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])

        begining_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.move_to(begining_translated_coords[0], begining_translated_coords[1])
        for i in range(1, len(self.normalized_coordinates)):
            next_translated_coords = viewport_function(self.normalized_coordinates[i][0], self.normalized_coordinates[i][1])
            context.line_to(next_translated_coords[0], next_translated_coords[1])

        next_translated_coords = viewport_function(self.normalized_coordinates[0][0], self.normalized_coordinates[0][1])
        context.line_to(next_translated_coords[0], next_translated_coords[1])

        context.set_line_width(2)
        context.stroke()