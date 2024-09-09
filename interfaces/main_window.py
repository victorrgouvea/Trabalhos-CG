from gi.repository import Gtk
from interfaces.button import Button
from interfaces.drawning_area import DrawingArea
from interfaces.display_file_interface import DisplayFileInterface

# <TODO> Create globals.py to store global variables
view_size = 852

class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Main Window")

        #Main Box
        self.set_default_size(1280, 1024) 
        self.Mainbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.connect("destroy", Gtk.main_quit)
        self.add(self.Mainbox)

        #Left Box
        self.LeftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.Mainbox.pack_start(self.LeftBox, True, True, 0)

        #Right Box
        self.RightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.Mainbox.pack_start(self.RightBox, True, True, 0)

        #Title
        self.title_label = Gtk.Label()
        self.title_label.set_markup("<b>Objetos</b>")
        self.LeftBox.add(self.title_label)

        ## <TODO> move those below to the system.py, where we will integrate different parts of the system

        #Drawing Area
        self.viewPort = DrawingArea(view_size)
        self.RightBox.add(self.viewPort.MainBox)
        
        #Display File Interface
        self.displayFileInterface = DisplayFileInterface()
        self.button = Button(self.displayFileInterface.add_row)
        self.LeftBox.add(self.displayFileInterface)
        self.LeftBox.add(self.button)

