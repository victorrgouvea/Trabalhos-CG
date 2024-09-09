from gi.repository import Gtk


class ObjectDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Incluir Objeto", transient_for=parent, flags=0)
        self.set_default_size(200, 200)
        self.selected_type = None

        # Caixa de conteúdo
        box = self.get_content_area()

        # Campo de texto para nome
        name_label = Gtk.Label(label="Nome")
        name_entry = Gtk.Entry()

        # Adicionando o campo de nome na área de conteúdo
        box.add(name_label)
        box.add(name_entry)

        # Criar um grupo de Radio Buttons para selecionar o tipo de objeto
        radio_box = Gtk.Box(spacing=6)

        point_button = Gtk.RadioButton.new_with_label_from_widget(None, "Point")
        line_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Line")
        wireframe_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Wireframe")

        # Conectar os botões ao método que armazena o valor
        point_button.connect("toggled", self.on_button_toggled, "point")
        line_button.connect("toggled", self.on_button_toggled, "line")
        wireframe_button.connect("toggled", self.on_button_toggled, "wireframe")

        # Adicionar os botões de radio ao layout
        radio_box.pack_start(point_button, True, True, 0)
        radio_box.pack_start(line_button, True, True, 0)
        radio_box.pack_start(wireframe_button, True, True, 0)

        box.add(radio_box)

        # Campo de texto para coordenadas (como no campo de nome)
        coordinates_label = Gtk.Label(label="Coordenadas (Ex: (x1, y1), (x2, y2)...)")
        coordinates_entry = Gtk.Entry()
        box.add(coordinates_label)
        box.add(coordinates_entry)

        # Botões OK e Cancelar
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        # Mostrar todos os widgets
        self.show_all()

    def on_button_toggled(self, button, object_type):
        if button.get_active():
            # Armazenar o valor selecionado em letras minúsculas
            self.selected_type = object_type