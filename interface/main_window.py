from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Main Window")
        # Define o tamanho da janela (largura, altura)
        self.set_default_size(800, 600)  # Exemplo de tamanho ideal
        self.connect("destroy", Gtk.main_quit)