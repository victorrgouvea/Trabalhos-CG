from gi.repository import Gtk, Gdk, Pango

class DrawingArea():

    def __init__(self, view_size, display_file):
        # Main  Box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("black"))
        #self.main_box.set_size_request(view_size + 20, view_size + 20)
        # Label
        self.label = Gtk.Label(label="ViewPort")
        self.label.modify_font(Pango.FontDescription("Sans 10"))
        self.label.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("white"))
        self.main_box.pack_start(self.label, True, True, 0)
        self.main_box.set_margin_start(20)
        self.main_box.set_margin_end(20)
        # Display File
        self.display_file = display_file

        # Drawing Area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(view_size, view_size)
        #self.drawing_area.set_margin_top(20)
        self.drawing_area.set_margin_bottom(20)
        self.drawing_area.set_margin_start(20)
        self.drawing_area.set_margin_end(20)
        self.drawing_area.connect("draw", self.on_draw)
        #self.drawing_area.set_hexpand(True)
        #self.drawing_area.set_vexpand(True)

    def on_draw(self, _, context):
        context.set_source_rgb(1, 1, 1)
        context.paint()
        self.display_file.draw(context)

    def force_redraw(self):
        self.drawing_area.queue_draw()