from pathlib import Path
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# Importa el widget para que el Builder lo conozca
import pantalla_dibujo          # noqa: F401
from pronunciador import clear_cache

Window.clearcolor = (1, 1, 1, 1)   # fondo blanco global


class DibloApp(App):
    kv_file = None                  # evitamos que Kivy cargue diblo.kv dos veces

    def build(self):
        kv_path = Path(__file__).with_name("diblo.kv")
        return Builder.load_file(str(kv_path))

    # Limpia la caché de audios al cerrar con normalidad
    def on_stop(self):
        clear_cache()


if __name__ == "__main__":
    try:
        DibloApp().run()
    finally:
        # Si la app se cierra por excepción, asegúrate de borrar la caché
        clear_cache()
