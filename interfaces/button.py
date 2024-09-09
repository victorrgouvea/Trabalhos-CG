from gi.repository import Gtk
from interfaces.object_dialog import ObjectDialog

class Button(Gtk.Button):
    def __init__(self, window):
        super().__init__(label="Add Object")
        self.window = window
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        dialog = ObjectDialog(self.window)
        dialog.run()  # Exibir a janela como um pop-up
        dialog.destroy()
