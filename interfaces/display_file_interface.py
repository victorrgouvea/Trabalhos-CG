from gi.repository import Gtk


class DisplayFileInterface(Gtk.ScrolledWindow):

    def __init__(self):
        super().__init__()
        self.set_size_request(200, 100)  # Definir tamanho fixo para a lista
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Criando uma ListBox para os objetos
        self.listbox = Gtk.ListBox()
        
        self.add(self.listbox)

    def add_row(self, name):
        item = Gtk.Label(label=name)
        self.listbox.add(item)
        self.listbox.show_all()
