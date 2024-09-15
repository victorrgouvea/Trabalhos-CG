from gi.repository import Gtk
from interfaces.new_object_dialog import NewObjectDialog
from interfaces.transform_object_dialog import TransformObjectDialog

class NewObjectButton(Gtk.Button):
    def __init__(self, window):
        super().__init__(label="Add Object")
        self.window = window
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        dialog = NewObjectDialog(self.window)
        dialog.run()  # Exibir a janela como um pop-up
        dialog.destroy()
        
class TransformObjectButton(Gtk.Button):
    def __init__(self, window):
        super().__init__(label="Transform Object")
        self.window = window
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        if self.window.display_file_interface.selected_item is not None:
            dialog = TransformObjectDialog(self.window)
            dialog.run()  # Exibir a janela como um pop-up
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "No object selected")
            dialog.format_secondary_text("Select a object to transform.")
            dialog.run()
            dialog.destroy()
