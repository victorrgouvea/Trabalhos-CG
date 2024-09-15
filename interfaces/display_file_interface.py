from gi.repository import Gtk


class DisplayFileInterface(Gtk.ScrolledWindow):

    def __init__(self):
        super().__init__()
        self.set_size_request(200, 100)  # Definir tamanho fixo para a lista
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.objects = {}
        self.selected_item = None
        
        # Criando uma ListBox para os objetos
        self.listbox = Gtk.ListBox()
        
        self.listbox.connect("row-selected", self.on_row_selected)
        
        self.add(self.listbox)

    def add_row(self, name, type, instance):
        item_str = type + "(" + name + ")"
        item = Gtk.Label(label=item_str)
        self.objects[item_str] = {
            'name': name,
            'instance': instance
        }
        
        self.listbox.add(item)
        self.listbox.show_all()
        
    def on_row_selected(self, listbox, row):
        if row is not None:
            label = row.get_child()
            name = label.get_text()
            self.selected_item = self.objects[name]
