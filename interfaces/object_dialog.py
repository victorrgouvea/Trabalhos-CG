from gi.repository import Gtk


class ObjectDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Add Object", transient_for=parent, flags=0)
        self.main_window = parent
        self.set_default_size(200, 200)
        self.selected_type = None
        self.names = []

        # Caixa de conteúdo
        box = self.get_content_area()

        # Campo de texto para nome
        self.name_label = Gtk.Label(label="Nome")
        self.name_entry = Gtk.Entry()

        # Adicionando o campo de nome na área de conteúdo
        box.add(self.name_label)
        box.add(self.name_entry)

        # Criar um grupo de Radio Buttons para selecionar o tipo de objeto
        radio_box = Gtk.Box(spacing=6)

        point_button = Gtk.RadioButton.new_with_label_from_widget(None, "Point")
        line_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Line")
        wireframe_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Wireframe")

        # Conectar os botões ao método que armazena o valor
        point_button.connect("toggled", self.on_button_toggled, "Point")
        line_button.connect("toggled", self.on_button_toggled, "Line")
        wireframe_button.connect("toggled", self.on_button_toggled, "Wireframe")

        # Checkboxes for type of object
        radio_box.pack_start(point_button, True, True, 0)
        radio_box.pack_start(line_button, True, True, 0)
        radio_box.pack_start(wireframe_button, True, True, 0)

        box.add(radio_box)

        # Entry for coordinates
        self.coordinates_label = Gtk.Label(label="Coordenadas (Ex: (x1, y1), (x2, y2)...)")
        self.coordinates_entry = Gtk.Entry()
        box.add(self.coordinates_label)
        box.add(self.coordinates_entry)

        # OK and cancel buttons
        ok_button = self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        ok_button.connect("clicked", self.on_ok_clicked)

        self.show_all()

    def on_button_toggled(self, button, object_type):
        print(object_type)
        self.selected_type = object_type

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Erro na entrada de coordenadas",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_ok_clicked(self, widget):

        if self.name_entry.get_text() not in self.names and self.selected_type is not None:
            
            # Add object to the display file object
            color = (0, 0, 0)

            # try:
            input_string = self.coordinates_entry.get_text().replace("(", "").replace(")", "").replace(" ", "")
            coordinate_pairs = input_string.split(",")
            coordinates = [(float(coordinate_pairs[i]), float(coordinate_pairs[i + 1])) for i in range(0, len(coordinate_pairs), 2)]
            # except Exception as e:
            #     print(e)
            #     return self.show_error_dialog("Invalid input format for coordinates")

            self.main_window.display_file.add_object(self.name_entry.get_text(), self.selected_type.lower(), coordinates, color)
            
            # Add object to the display interface
            self.main_window.display_file_interface.add_row(f"{self.selected_type}({self.name_entry.get_text()})")

            self.names.append(self.name_entry.get_text())
