from gi.repository import Gtk

class ControlPanel(Gtk.Box):
    def __init__(self, main_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_window = main_window

        self.panning_label = Gtk.Label()
        self.panning_label.set_markup("<b>Panning</b>")
        self.pack_start(self.panning_label, False, False, 0)

        # Criando um grid para os botões de movimentação (Up, Down, Left, Right)
        move_grid = Gtk.Grid()
        move_grid.set_row_spacing(10)
        move_grid.set_column_spacing(5)

        # Botões de movimentação
        self.up_button = Gtk.Button(label="Up")
        self.down_button = Gtk.Button(label="Down")
        self.left_button = Gtk.Button(label="Left")
        self.right_button = Gtk.Button(label="Right")

        self.up_button.connect("clicked", self.on_up_clicked)
        self.down_button.connect("clicked", self.on_down_clicked)
        self.left_button.connect("clicked", self.on_left_clicked)
        self.right_button.connect("clicked", self.on_right_clicked)

        # Adicionar os botões no grid
        move_grid.attach(self.up_button, 1, 0, 1, 1)     # Botão "Up" no centro superior
        move_grid.attach(self.left_button, 0, 1, 1, 1)   # Botão "Left" no centro esquerdo
        move_grid.attach(self.right_button, 2, 1, 1, 1)  # Botão "Right" no centro direito
        move_grid.attach(self.down_button, 1, 2, 1, 1)   # Botão "Down" no centro inferior


        align_grid = Gtk.Alignment.new(0.5, 0, 0, 0)
        align_grid.add(move_grid)

        # Adicionar o grid ao layout principal
        self.pack_start(align_grid, True, True, 0)

        self.panning_label = Gtk.Label()
        self.panning_label.set_markup("<b>Navigation</b>")
        self.pack_start(self.panning_label, False, False, 0)

        move_grid2 = Gtk.Grid()
        move_grid2.set_row_spacing(10)
        move_grid2.set_column_spacing(5)

        # Navigation buttons
        self.front_button = Gtk.Button(label="Front")
        self.back_button = Gtk.Button(label="Back")
        self.inward_left_button = Gtk.Button(label="Inward Left")
        self.inward_right_button = Gtk.Button(label="Inward Right")

        self.front_button.connect("clicked", self.on_front_clicked)
        self.back_button.connect("clicked", self.on_back_clicked)
        self.inward_left_button.connect("clicked", self.on_inward_left_clicked)
        self.inward_right_button.connect("clicked", self.on_inward_right_clicked)

        move_grid2.attach(self.front_button, 1, 3, 1, 1)  # Botão "Front"
        move_grid2.attach(self.back_button, 1, 5, 1, 1)   # Botão "Back"
        move_grid2.attach(self.inward_left_button, 0, 4, 1, 1)   # Botão "Inward Left"
        move_grid2.attach(self.inward_right_button, 2, 4, 1, 1)  # Botão "Inward Right"

        align_grid2 = Gtk.Alignment.new(0.5, 0, 0, 0)
        align_grid2.add(move_grid2)

        self.pack_start(align_grid2, True, True, 0)

        self.rotation_label = Gtk.Label()
        self.rotation_label.set_markup("<b>Rotation</b>")
        self.pack_start(self.rotation_label, False, False, 0)

        # Caixa para os botões de rotação e o campo de entrada
        rotation_box = Gtk.Box(spacing=6)

        self.rotate_left_button = Gtk.Button(label="⟲")
        self.rotate_right_button = Gtk.Button(label="⟳")
        self.angle_entry = Gtk.Entry()
        self.angle_entry.set_placeholder_text("Angle")

        self.rotate_left_button.connect("clicked", self.on_rotate_left_clicked)
        self.rotate_right_button.connect("clicked", self.on_rotate_right_clicked)

        # Adicionar os botões e a entrada ao layout de rotação
        rotation_box.pack_start(self.angle_entry, True, True, 0)
        rotation_box.pack_start(self.rotate_left_button, True, True, 0)
        rotation_box.pack_start(self.rotate_right_button, True, True, 0)

        align_grid = Gtk.Alignment.new(0.5, 0, 0, 0)
        align_grid.add(rotation_box)

        self.pack_start(align_grid, True, True, 0)

        zoom_box = Gtk.Box(spacing=6)

        self.zoom_label = Gtk.Label()
        self.zoom_label.set_markup("<b>Zoom</b>")

        self.zoom_in_button = Gtk.Button(label="+")
        self.zoom_out_button = Gtk.Button(label="-")

        self.zoom_in_button.connect("clicked", self.on_zoom_in_clicked)
        self.zoom_out_button.connect("clicked", self.on_zoom_out_clicked)

        # Adicionar botões de Zoom ao layout horizontal
        zoom_box.pack_start(self.zoom_label, True, True, 0)
        zoom_box.pack_start(self.zoom_in_button, True, True, 0)
        zoom_box.pack_start(self.zoom_out_button, True, True, 0)

        self.pack_start(zoom_box, True, True, 0)

        self.clip_label = Gtk.Label()
        self.clip_label.set_markup("<b>Line Clipping</b>")
        self.pack_start(self.clip_label, False, False, 0)

        clip_box = Gtk.Box(spacing=6)

        # Adicionar RadioButtons para a escolha de algoritmos de clipagem
        self.cohen_sutherland_button = Gtk.RadioButton.new_with_label_from_widget(None, "Cohen-Sutherland")
        self.liang_barsky_button = Gtk.RadioButton.new_with_label_from_widget(self.cohen_sutherland_button, "Liang-Barsky")

        self.cohen_sutherland_button.connect("toggled", self.on_clipping_method_toggled, "cohen-sutherland")
        self.liang_barsky_button.connect("toggled", self.on_clipping_method_toggled, "liang_barsky")

        clip_box.pack_start(self.cohen_sutherland_button, True, True, 0)
        clip_box.pack_start(self.liang_barsky_button, True, True, 0)

        self.pack_start(clip_box, True, True, 0)

    def on_up_clicked(self, _):
        self.main_window.window.change_offset(0, 10)
        self.main_window.drawing_area.force_redraw()

    def on_down_clicked(self, _):
        self.main_window.window.change_offset(0, -10)
        self.main_window.drawing_area.force_redraw()

    def on_left_clicked(self, _):
        self.main_window.window.change_offset(-10, 0)
        self.main_window.drawing_area.force_redraw()

    def on_right_clicked(self, _):
        self.main_window.window.change_offset(10, 0)
        self.main_window.drawing_area.force_redraw()

    def on_inward_left_clicked(self, _):
        self.main_window.window.rotate_axis_y(15)
        self.main_window.drawing_area.force_redraw()

    def on_inward_right_clicked(self, _):
        self.main_window.window.rotate_axis_y(-15)
        self.main_window.drawing_area.force_redraw()

    def on_front_clicked(self, _):
        # self.main_window.window.change_offset(0, 0)
        # self.main_window.drawing_area.force_redraw()
        pass
    
    def on_back_clicked(self, _):
        # self.main_window.window.change_offset(0, 0)
        # self.main_window.drawing_area.force_redraw()
        pass

    def on_zoom_out_clicked(self, _):
        self.main_window.window.change_zoom(1.05, 1.05)
        self.main_window.drawing_area.force_redraw()

    def on_zoom_in_clicked(self, _):
        self.main_window.window.change_zoom(0.95, 0.95)
        self.main_window.drawing_area.force_redraw()

    def on_rotate_left_clicked(self, _):
        angle = self.get_angle()
        if angle is not None:
            self.main_window.window.rotate([0, 0, -angle])
            self.main_window.drawing_area.force_redraw()

    def on_rotate_right_clicked(self, _):
        angle = self.get_angle()
        if angle is not None:
            self.main_window.window.rotate([0, 0, angle])
            self.main_window.drawing_area.force_redraw()

    def on_clipping_method_toggled(self, button, method):
        if button.get_active():
            self.main_window.display_file.clip_algorithm = method

    def key_handler(self, key):
        key = key.lower()

        match key:
            case "w":
                self.on_up_clicked(None)
            case "s":
                self.on_down_clicked(None)
            case "a":
                self.on_left_clicked(None)
            case "d":
                self.on_right_clicked(None)
            case "+":
                self.on_zoom_in_clicked(None)
            case "-":
                self.on_zoom_out_clicked(None)

    def get_angle(self):
        try:
            return float(self.angle_entry.get_text())
        except:
            dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Invalid angle for rotation")
            dialog.format_secondary_text("Choose a valid angle to rotate the world.")
            dialog.run()
            dialog.destroy()
