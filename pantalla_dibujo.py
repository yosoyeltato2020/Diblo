from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.clock import Clock
import config
import reconocimiento
from palabras import Palabras
import logging
from pathlib import Path
from datetime import datetime
import pronunciador

logger = logging.getLogger(__name__)

class PantallaDibujo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gestor_palabras = Palabras()
        self.categorias = self.gestor_palabras.get_categorias()

    def on_kv_post(self, base_widget):
        color_grid = self.ids.color_buttons_grid
        color_grid.clear_widgets()
        for color in config.PALETA_COLORES:
            btn = Button(
                background_normal='',
                background_color=color,
                size_hint=(1, 1),
                on_release=lambda b, c=color: self.ids.drawing_area.set_color(c)
            )
            color_grid.add_widget(btn)

    def set_categoria(self, nombre_categoria):
        if nombre_categoria == "Todas las categorías":
            self.gestor_palabras._set_default_list()
        else:
            self.gestor_palabras.set_categoria(nombre_categoria)
        self.generar_nueva_palabra()

    def generar_nueva_palabra(self):
        palabra = self.gestor_palabras.nueva_palabra()
        self.ids.lbl_palabra_base_text.text = palabra

    def borrar_dibujo(self):
        self.ids.drawing_area.clear_canvas()

    def guardar_dibujo(self):
        palabra = self.ids.lbl_palabra_base_text.text or "dibujo"
        nombre_archivo = f"{palabra}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        ruta = Path("dibujos") / nombre_archivo
        ruta.parent.mkdir(exist_ok=True)
        resultado = self.ids.drawing_area.export_to_png(str(ruta))
        if resultado:
            logger.info(f"Dibujo guardado en: {ruta}")
        else:
            logger.warning("No se pudo guardar el dibujo.")

    def pronunciar_palabra(self):
        palabra = self.ids.lbl_palabra_base_text.text.strip()
        if palabra:
            pronunciador.reproducir_palabra(palabra)

    def iniciar_reconocimiento_voz(self):
        pronunciador.reproducir_inicio_grabacion()
        palabra = reconocimiento.reconocer_voz()
        pronunciador.reproducir_fin_grabacion()
        if palabra:
            self.ids.lbl_mensaje_voz.text = palabra
        else:
            self.ids.lbl_mensaje_voz.text = "No se entendió"

    def go_to_main_menu(self):
        self.manager.current = "welcome_screen"
