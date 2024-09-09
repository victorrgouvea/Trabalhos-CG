from gi.repository import Gtk
from interfaces.main_window import MainWindow

#Interactive Graphic System
class IGS:
    def __init__(self):
        self.window = MainWindow()
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()