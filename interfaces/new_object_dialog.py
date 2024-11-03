from gi.repository import Gtk


class NewObjectDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Add Object", transient_for=parent, flags=0)
        self.main_window = parent
        self.set_default_size(200, 200)
        self.selected_type = "Point"
        self.names = []
        self.fill_wireframe = False  # Para verificar se o polígono será desenhado

        box = self.get_content_area()

        self.name_label = Gtk.Label(label="Name")
        self.name_entry = Gtk.Entry()

        box.add(self.name_label)
        box.add(self.name_entry)

        radio_box = Gtk.Box(spacing=6)

        point_button = Gtk.RadioButton.new_with_label_from_widget(None, "Point")
        line_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Line")
        wireframe_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Wireframe")
        bezier_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Bezier Curve")
        spline_button = Gtk.RadioButton.new_with_label_from_widget(point_button, "Spline Curve")

        point_button.connect("toggled", self.on_button_toggled, "Point")
        line_button.connect("toggled", self.on_button_toggled, "Line")
        wireframe_button.connect("toggled", self.on_button_toggled, "Wireframe")
        bezier_button.connect("toggled", self.on_button_toggled, "Bezier Curve")
        spline_button.connect("toggled", self.on_button_toggled, "Spline Curve")

        # Checkboxes for type of object
        radio_box.pack_start(point_button, True, True, 0)
        radio_box.pack_start(line_button, True, True, 0)
        radio_box.pack_start(wireframe_button, True, True, 0)
        radio_box.pack_start(bezier_button, True, True, 0)
        radio_box.pack_start(spline_button, True, True, 0)

        box.add(radio_box)

        self.draw_polygon_checkbox = Gtk.CheckButton(label="Fill Wireframe?")
        self.draw_polygon_checkbox.connect("toggled", self.on_draw_polygon_toggled)
        box.add(self.draw_polygon_checkbox)

        # Entry for coordinates
        self.coordinates_label = Gtk.Label(label="Coordinates (Ex: (x1, y1, z1), (x2, y2, z2)...)")
        self.coordinates_entry = Gtk.Entry()
        box.add(self.coordinates_label)
        box.add(self.coordinates_entry)

        self.color_button = Gtk.ColorButton()
        self.color_button.set_title("Color")
        box.add(Gtk.Label(label="Color:"))
        box.add(self.color_button)

        # OK and cancel buttons
        ok_button = self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        ok_button.connect("clicked", self.on_ok_clicked)

        self.show_all()

        self.draw_polygon_checkbox.hide()

    def on_button_toggled(self, button, object_type):
        self.selected_type = object_type

        if object_type == "Wireframe":
            self.draw_polygon_checkbox.show()
        else:
            self.draw_polygon_checkbox.hide()

    def on_draw_polygon_toggled(self, button):
        self.fill_wireframe = button.get_active()

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Input value error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_ok_clicked(self, widget):

        if (self.name_entry.get_text() not in [obj['name'] for obj in self.main_window.display_file_interface.objects.values()]
            and self.selected_type is not None):
            
            rgba = self.color_button.get_rgba()
            color = (rgba.red, rgba.green, rgba.blue) 

            try:
                input_string = self.coordinates_entry.get_text().replace("(", "").replace(")", "").replace(" ", "")
                coordinate_pairs = input_string.split(",")
                coordinates = [(float(coordinate_pairs[i]), float(coordinate_pairs[i + 1]), float(coordinate_pairs[i + 2])) for i in range(0, len(coordinate_pairs), 3)]
            except Exception as e:
                print(e)
                return self.show_error_dialog("Invalid input format for coordinates")

            # Only accepts when all curves are completed
            if ((self.selected_type == "Bezier Curve" or self.selected_type == "Spline Curve") and 
                not (len(coordinates) == 4 or (len(coordinates) > 4 and len(coordinates) % 4 == 3))):

                return self.show_error_dialog("Invalid number of points for Bezier Curve")

            # Fill wireframe if selected
            if self.selected_type == "Wireframe" and self.fill_wireframe:
                created_object = self.main_window.display_file.add_object(self.name_entry.get_text(), self.selected_type.lower(), coordinates, color, True)
            else:
                created_object = self.main_window.display_file.add_object(self.name_entry.get_text(), self.selected_type.lower(), coordinates, color)

            self.main_window.display_file_interface.add_row(self.name_entry.get_text(), self.selected_type, created_object)

            self.main_window.drawing_area.force_redraw()
            
        else:
            self.show_error_dialog("Duplicated name or type not selected")
