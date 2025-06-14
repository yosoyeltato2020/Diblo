from kivy.app import App
from kivy.lang import Builder
from pantalla_dibujo import DibujoWidget  # registra la clase para el Builder
from kivy.core.window import Window

# Color de fondo blanco global
Window.clearcolor = (1, 1, 1, 1)

class DibloApp(App):
    def build(self):
        # Carga la interfaz declarada en diblo.kv
        return Builder.load_file("diblo.kv")

if __name__ == "__main__":
    DibloApp().run()
