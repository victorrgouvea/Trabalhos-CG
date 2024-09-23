from gi.repository import Gtk
from interfaces.new_object_dialog import NewObjectDialog
from interfaces.transform_object_dialog import TransformObjectDialog
from interfaces.file_name_dialog import FileNameDialog
from system.file_system import FileSystem

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

class LoadFileButton(Gtk.Button):
    def __init__(self, window):
        super().__init__(label="Load Object File")
        self.window = window
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_obj = Gtk.FileFilter()
        filter_obj.set_name("Arquivos OBJ")
        filter_obj.add_pattern("*.obj")
        dialog.add_filter(filter_obj)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            print(f'File selected: {filename}')

            # Chama a função para carregar o arquivo
            file_system = FileSystem(self.window)
            file_system.load_file(filename)

            if not filename.endswith('.obj'):
                dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Invalid file")
                dialog.format_secondary_text("Select a .obj file.")
                dialog.run()
                dialog.destroy()

        dialog.destroy()

class SaveFileButton(Gtk.Button):
    def __init__(self, window):
        super().__init__(label="Save Object File")
        self.window = window
        self.connect("clicked", self.on_button_clicked)
    
    def on_button_clicked(self, widget):
        if len(self.window.display_file.objects) > 0:
            dialog = FileNameDialog(self.window)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                filename = dialog.get_filename()

                if filename:
                    if not filename.endswith('.obj'):
                        filename += '.obj'

                    path = f'./assets/objects/{filename}'

                    # Chama a função para criar o arquivo
                    file_system = FileSystem(self.window)
                    file_system.save_file(path, self.window.display_file.objects)

                else:
                    aux_dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "No file name")
                    aux_dialog.format_secondary_text("Enter a file name.")
                    aux_dialog.run()
                    aux_dialog.destroy()
            
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "No object created")
            dialog.format_secondary_text("Create a object to save world as a .obj file.")
            dialog.run()
            dialog.destroy()
