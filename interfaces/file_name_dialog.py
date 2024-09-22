from gi.repository import Gtk

class FileNameDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Nome do Arquivo", parent=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(200, 100)

        # Criação de uma entrada para o nome do arquivo
        box = self.get_content_area()
        self.entry = Gtk.Entry()
        self.entry.set_text("new_file.obj")  # Valor padrão para o arquivo
        box.add(self.entry)
        self.show_all()

    def get_filename(self):
        return self.entry.get_text()