from objects.generic3d_object import Generic3dObject


class Wireframe3D(Generic3dObject):

    def __init__(self, name, coordinates, color, fill):
        super().__init__(name, 'wireframe', coordinates, color, fill)

    def draw(self, context, viewport_function):
        context.new_path()
        context.set_source_rgb(self.color[0], self.color[1], self.color[2])
        context.set_line_width(2)
        screen_lines = [] 
        for i in range(len(self.clipped_lines)):
            point_a = viewport_function(self.clipped_lines[i][0][0], self.clipped_lines[i][0][1])
            point_b = viewport_function(self.clipped_lines[i][1][0], self.clipped_lines[i][1][1])
            screen_lines.append([point_a, point_b])

        if self.fill and len(screen_lines) > 0:
                context.move_to(screen_lines[0][0][0], screen_lines[0][0][1])

        for line in screen_lines:
            if self.fill:
                context.line_to(line[1][0], line[1][1])
            else:
                context.move_to(line[0][0], line[0][1])
                context.line_to(line[1][0], line[1][1])
                context.stroke()

        context.close_path()

        if self.fill:
            context.fill()