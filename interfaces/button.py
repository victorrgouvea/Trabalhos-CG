from gi.repository import Gtk
from interfaces.object_dialog import ObjectDialog

class Button(Gtk.Button):
    def __init__(self, function):
        super().__init__(label="Add Object")
        self.function = function
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        dialog = ObjectDialog(self)
        dialog.run()  # Exibir a janela como um pop-up
        dialog.destroy()
