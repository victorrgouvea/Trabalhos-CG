from gi.repository import Gtk
from interface.main_window import MainWindow

class System:
    def __init__(self):
        self.window = MainWindow()
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()