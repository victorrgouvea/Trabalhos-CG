from gi.repository import Gtk


class ObjectDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Incluir Objeto", transient_for=parent, flags=0)
        self.set_default_size(200, 200)

        # Caixa de conteúdo
        box = self.get_content_area()

        # Campo de texto para nome
        name_label = Gtk.Label(label="Nome")
        name_entry = Gtk.Entry()

        # Layout para coordenadas
        frame = Gtk.Frame(label="Coordenadas do Ponto Inicial")
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # Campos para coordenadas
        x1_entry = Gtk.Entry()
        y1_entry = Gtk.Entry()
        z1_entry = Gtk.Entry()
        x1_entry.set_text("x1")
        y1_entry.set_text("y1")
        z1_entry.set_text("z1")

        grid.attach(Gtk.Label(label="x1:"), 0, 0, 1, 1)
        grid.attach(x1_entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="y1:"), 0, 1, 1, 1)
        grid.attach(y1_entry, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label="z1:"), 0, 2, 1, 1)
        grid.attach(z1_entry, 1, 2, 1, 1)

        frame.add(grid)
        box.add(name_label)
        box.add(name_entry)
        box.add(frame)

        # Botões OK e Cancelar (padrão do Dialog)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.show_all()