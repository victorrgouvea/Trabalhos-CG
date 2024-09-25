from gi.repository import Gtk


class TransformObjectDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Transform Object", transient_for=parent, flags=0)

        self.main_window = parent
        self.pending_transformations = []
        self.selected_object = self.main_window.display_file_interface.selected_item['instance']
        self.set_default_size(500, 300)

        main_box = self.get_content_area()
        layout = Gtk.Box(spacing=10)
        main_box.pack_start(layout, True, True, 0)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layout.pack_start(left_box, True, True, 0)

        self.left_title_label = Gtk.Label()
        self.left_title_label.set_markup("<b>Transformations</b>")

        self.trans_button = Gtk.RadioButton.new_with_label_from_widget(None, "Translation")
        self.scale_button = Gtk.RadioButton.new_with_label_from_widget(self.trans_button, "Scaling")
        self.rotate_button = Gtk.RadioButton.new_with_label_from_widget(self.trans_button, "Rotation")

        self.trans_button.set_active(True)

        self.trans_button.connect("toggled", self.on_option_selected)
        self.scale_button.connect("toggled", self.on_option_selected)
        self.rotate_button.connect("toggled", self.on_option_selected)

        left_box.pack_start(self.left_title_label, False, False, 0)
        left_box.pack_start(self.trans_button, False, False, 0)
        left_box.pack_start(self.scale_button, False, False, 0)
        left_box.pack_start(self.rotate_button, False, False, 0)

        self.dynamic_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_box.pack_start(self.dynamic_area, True, True, 0)

        # Add button "Add" below the dynamic area
        add_button = Gtk.Button(label="Add")
        add_button.connect("clicked", self.on_add_button_clicked)
        left_box.pack_start(add_button, False, False, 0)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layout.pack_start(right_box, True, True, 0)

        self.right_title_label = Gtk.Label()
        self.right_title_label.set_markup("<b>List to be applied</b>")

        # ScrolledWindow to show the list of transformations
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_size_request(350, 200)

        # ListBox to store the transformations
        self.transformation_list = Gtk.ListBox()
        self.scrolled_window.add(self.transformation_list)

        right_box.pack_start(self.right_title_label, False, False, 0)
        right_box.pack_start(self.scrolled_window, True, True, 0)

        ok_button = self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        ok_button.connect("clicked", self.on_ok_button_clicked)  # Connect the OK button to a function
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        self.on_option_selected(self.trans_button)

        self.show_all()

    def on_option_selected(self, button):
        for child in self.dynamic_area.get_children():
            self.dynamic_area.remove(child)

        if self.trans_button.get_active():
            self.show_translation_inputs()
        elif self.scale_button.get_active():
            self.show_scaling_inputs()
        elif self.rotate_button.get_active():
            self.show_rotation_inputs()

        self.dynamic_area.show_all()

    # Inputs for the "Translation" option
    def show_translation_inputs(self):
        label = Gtk.Label(label="Specify values for X and Y:")
        self.entry_x = Gtk.Entry()
        self.entry_x.set_placeholder_text("X")
        self.entry_y = Gtk.Entry()
        self.entry_y.set_placeholder_text("Y")

        # Add to the dynamic layout
        self.dynamic_area.pack_start(label, False, False, 0)
        self.dynamic_area.pack_start(self.entry_x, False, False, 0)
        self.dynamic_area.pack_start(self.entry_y, False, False, 0)

    # Inputs for the "Scaling" option
    def show_scaling_inputs(self):
        label = Gtk.Label(label="Specify values for X and Y:")
        self.entry_x = Gtk.Entry()
        self.entry_x.set_placeholder_text("X")
        self.entry_y = Gtk.Entry()
        self.entry_y.set_placeholder_text("Y")

        self.dynamic_area.pack_start(label, False, False, 0)
        self.dynamic_area.pack_start(self.entry_x, False, False, 0)
        self.dynamic_area.pack_start(self.entry_y, False, False, 0)

    # Inputs for the "Rotation" option
    def show_rotation_inputs(self):
        label = Gtk.Label(label="Select the type and specify the angle:")
        self.angle_entry = Gtk.Entry()
        self.angle_entry.set_placeholder_text("Angle")

        # Radio buttons for types of rotation
        self.center_world_button = Gtk.RadioButton.new_with_label_from_widget(None, "Around the world center")
        self.center_object_button = Gtk.RadioButton.new_with_label_from_widget(self.center_world_button, "Around the object center")
        self.arbitrary_point_button = Gtk.RadioButton.new_with_label_from_widget(self.center_world_button, "Around an arbitrary point")

        # Connect the arbitrary point button to display X and Y fields
        self.arbitrary_point_button.connect("toggled", self.on_arbitrary_point_selected)

        self.dynamic_area.pack_start(label, False, False, 0)
        self.dynamic_area.pack_start(self.center_world_button, False, False, 0)
        self.dynamic_area.pack_start(self.center_object_button, False, False, 0)
        self.dynamic_area.pack_start(self.arbitrary_point_button, False, False, 0)
        self.dynamic_area.pack_start(self.angle_entry, False, False, 0)

    # Show X and Y fields for the arbitrary point
    def on_arbitrary_point_selected(self, button):
        for child in self.dynamic_area.get_children():
            if isinstance(child, Gtk.Entry) and (child.get_placeholder_text() == "X (arbitrary)" or child.get_placeholder_text() == "Y (arbitrary)"):
                self.dynamic_area.remove(child)

        if self.arbitrary_point_button.get_active():
            self.entry_x_arbitrary = Gtk.Entry()
            self.entry_x_arbitrary.set_placeholder_text("X (arbitrary)")
            self.entry_y_arbitrary = Gtk.Entry()
            self.entry_y_arbitrary.set_placeholder_text("Y (arbitrary)")

            self.dynamic_area.pack_start(self.entry_x_arbitrary, False, False, 0)
            self.dynamic_area.pack_start(self.entry_y_arbitrary, False, False, 0)

        self.dynamic_area.show_all()

    # Function to handle the "Add" button click
    def on_add_button_clicked(self, widget):
        if self.trans_button.get_active() and self.validate_coords(self.entry_x.get_text(), self.entry_y.get_text()):
            self.pending_transformations.append(("T", float(self.entry_x.get_text()), float(self.entry_y.get_text())))
            transformation = f"Translation: X = {float(self.entry_x.get_text())}, Y = {float(self.entry_y.get_text())}"

        elif self.scale_button.get_active() and self.validate_coords(self.entry_x.get_text(), self.entry_y.get_text()):
            self.pending_transformations.append(("S", float(self.entry_x.get_text()), float(self.entry_y.get_text())))
            transformation = f"Scaling: X = {float(self.entry_x.get_text())}, Y = {float(self.entry_y.get_text())}"

        elif self.rotate_button.get_active() and self.validate_angle(self.angle_entry.get_text()):

            if self.center_world_button.get_active():
                self.pending_transformations.append(("R", float(self.angle_entry.get_text()), "world"))
                rotation_type = "Around the world center"

            elif self.center_object_button.get_active():
                self.pending_transformations.append(("R", float(self.angle_entry.get_text()), "object"))
                rotation_type = "Around the object center"

            elif self.arbitrary_point_button.get_active() and self.validate_coords(self.entry_x_arbitrary.get_text(), self.entry_y_arbitrary.get_text()):
                self.pending_transformations.append(("R", float(self.angle_entry.get_text()), "arbitrary", [float(self.entry_x_arbitrary.get_text()), float(self.entry_y_arbitrary.get_text())]))
                rotation_type = f"Around arbitrary point: X = {float(self.entry_x_arbitrary.get_text())}, Y = {float(self.entry_y_arbitrary.get_text())}"

            transformation = f"Rotation ({rotation_type}): Angle = {float(self.angle_entry.get_text())}"

        self.add_transformation(transformation)


    def on_ok_button_clicked(self, widget):
        self.selected_object.transform(self.pending_transformations)
        self.selected_object.apply_normalization(self.main_window.window.get_normalized_matrix())
        self.main_window.view_port.force_redraw()

    def add_transformation(self, transformation):
        row = Gtk.ListBoxRow()
        label = Gtk.Label(label=transformation)
        label.set_xalign(0)
        row.add(label)
        self.transformation_list.add(row)
        self.transformation_list.show_all()

    def validate_coords(self, x, y):
        try:
            x = float(x)
            y = float(y)
            return True
        except ValueError:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=Gtk.DialogFlags.MODAL,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format="Please enter valid numeric values for X and Y"
            )
            dialog.run()
            dialog.destroy()

            return False

    def validate_angle(self, angle):
        try:
            angle = float(angle)
            return True
        except ValueError:
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=Gtk.DialogFlags.MODAL,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                message_format="Please enter a valid numeric value for Angle."
            )
            dialog.run()
            dialog.destroy()

            return False
