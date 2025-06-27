from kivy.uix.screenmanager import Screen
from palabras import Palabras

class PantallaDibujo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gestor_palabras = Palabras()  # Instancia la clase
        self.categorias = self.gestor_palabras.get_categorias()
        # Si quieres usar las categorías para un spinner:
        # (asumiendo que tienes el spinner en self.ids.spinner_categorias_id)
        # Esto solo después de que el widget está cargado, usa on_kv_post si hace falta

    def on_kv_post(self, base_widget):
        # Llenar el spinner de categorías una vez cargada la interfaz
        self.ids.spinner_categorias_id.values = ["Todas las categorías"] + self.gestor_palabras.get_categorias()

    def generar_nueva_palabra(self):
        palabra = self.gestor_palabras.nueva_palabra()
        self.ids.lbl_palabra_base_text.text = palabra

    def on_spinner_category_selected(self, spinner, text):
        if text == "Todas las categorías":
            self.gestor_palabras._set_default_list()
        else:
            self.gestor_palabras.set_categoria(text)
        self.generar_nueva_palabra()

    def borrar_dibujo(self):
        self.ids.drawing_area.clear_canvas()

    def guardar_dibujo(self):
        # Tu lógica para guardar
        pass

    def pronunciar_palabra(self):
        # Tu lógica de pronunciador
        pass

    def iniciar_reconocimiento_voz(self):
        # Tu lógica de reconocimiento
        pass

    def go_to_main_menu(self):
        self.manager.current = "welcome_screen"
