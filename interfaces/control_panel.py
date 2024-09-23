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
        move_grid.set_row_spacing(5)
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

        self.rotation_label = Gtk.Label()
        self.rotation_label.set_markup("<b>Rotação</b>")
        self.pack_start(self.rotation_label, False, False, 0)

        # Caixa para os botões de rotação e o campo de entrada
        rotation_box = Gtk.Box(spacing=6)

        self.rotate_left_button = Gtk.Button(label="⟲")
        self.rotate_right_button = Gtk.Button(label="⟳")
        self.angle_entry = Gtk.Entry()
        self.angle_entry.set_placeholder_text("Ângulo")

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

    def on_up_clicked(self, _):
        self.main_window.window.change_offset(0, 10)
        self.main_window.view_port.force_redraw()

    def on_down_clicked(self, _):
        self.main_window.window.change_offset(0, -10)
        self.main_window.view_port.force_redraw()

    def on_left_clicked(self, _):
        self.main_window.window.change_offset(-10, 0)
        self.main_window.view_port.force_redraw()

    def on_right_clicked(self, _):
        self.main_window.window.change_offset(10, 0)
        self.main_window.view_port.force_redraw()

    def on_zoom_out_clicked(self, _):
        self.main_window.window.change_zoom(-10, 10)
        self.main_window.view_port.force_redraw()

    def on_zoom_in_clicked(self, _):
        self.main_window.window.change_zoom(10, -10)
        self.main_window.view_port.force_redraw()

    def on_rotate_left_clicked(self, _):
        # angle = self.get_angle()
        # if angle is not None:
        #     self.main_window.window.rotate(-angle)
        #     self.main_window.view_port.force_redraw()
        pass

    def on_rotate_right_clicked(self, _):
        # angle = self.get_angle()
        # if angle is not None:
        #     self.main_window.window.rotate(angle)
        #     self.main_window.view_port.force_redraw()
        pass

    def get_angle(self):
        try:
            return float(self.angle_entry.get_text())
        except:
            dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Invalid angle for rotation")
            dialog.format_secondary_text("Choose a valid angle to rotate the world.")
            dialog.run()
            dialog.destroy()
        