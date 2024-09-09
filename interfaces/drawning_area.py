from gi.repository import Gtk, Gdk, Pango


class DrawingArea():

    def __init__(self, view_size):
        # Main  Box
        self.MainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.MainBox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("black"))

        # Label
        self.label = Gtk.Label(label="ViewPort")
        self.label.modify_font(Pango.FontDescription("Sans 10"))
        self.label.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("white"))
        self.MainBox.pack_start(self.label, True, True, 0)

        # Drawing Area
        self.drawingArea = Gtk.DrawingArea()
        self.drawingArea.set_size_request(view_size, view_size)
        self.drawingArea.set_margin_top(20)
        self.drawingArea.set_margin_bottom(20)
        self.drawingArea.set_margin_start(20)
        self.drawingArea.set_margin_end(20)
        self.drawingArea.connect("draw", self.on_draw)
        #self.drawingArea.set_hexpand(True)
        #self.drawingArea.set_vexpand(True)

    def on_draw(self, _, cr):
        cr.set_source_rgb(0.7, 0.3, 0.9)
        cr.paint()

    def force_redraw(self):
        self.drawingArea.queue_draw()