from gi.repository import Gtk
from interfaces.buttons import NewObjectButton, TransformObjectButton, LoadFileButton, SaveFileButton
from interfaces.drawning_area import DrawingArea
from interfaces.display_file_interface import DisplayFileInterface
from interfaces.control_panel import ControlPanel
from system.view_port import ViewPort
from system.window import Window
from system.display_file import DisplayFile

# <TODO> Create globals.py to store global variables
view_size = 852

class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Main Window")

        # Main Box
        self.set_default_size(1280, 1280) 
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.connect("destroy", Gtk.main_quit)
        self.add(self.main_box)

        # Left Box
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.main_box.pack_start(self.left_box, True, True, 0)

        # Right Box
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.main_box.pack_start(self.right_box, True, True, 0)

        #Title
        self.title_label = Gtk.Label()
        self.title_label.set_markup("<b>Objects</b>")
        self.left_box.add(self.title_label)

        ## <TODO> move those below to the system.py, where we will integrate different parts of the system
        
        # window 
        self.window = Window(1280, 1280)

        # view port
        self.viewPort = ViewPort(view_size, view_size, self.window)

        # Display File Interface
        self.display_file = DisplayFile(self.viewPort)
        self.display_file_interface = DisplayFileInterface()
        self.new_object_dialog_button = NewObjectButton(self)
        self.transform_object_dialog_button = TransformObjectButton(self)
        self.load_file_button = LoadFileButton(self)
        self.save_file_button = SaveFileButton(self)
        self.left_box.add(self.display_file_interface)
        self.left_box.add(self.new_object_dialog_button)
        self.left_box.add(self.transform_object_dialog_button)
        self.left_box.add(self.load_file_button)
        self.left_box.add(self.save_file_button)

        # Control panel
        self.control_panel = ControlPanel(self)
        self.left_box.add(self.control_panel)

        # Drawing Area
        self.view_port = DrawingArea(view_size, self.display_file)
        self.right_box.add(self.view_port.main_box)
        self.right_box.add(self.view_port.drawing_area)





