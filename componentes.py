# componentes.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.utils import get_color_from_hex
from kivy.app import App
from functools import partial
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.metrics import dp # Importar dp

import logging

logger = logging.getLogger(__name__)

class DrawingArea(Widget):
    """
    Lienzo interactivo donde el usuario puede dibujar con trazos de color.

    Permite cambiar el color de dibujo y borrar todo el contenido.
    Detecta eventos táctiles para dibujar líneas continuas.
    """

    def __init__(self, **kwargs):
        """
        Inicializa DrawingArea con un color de dibujo por defecto y un fondo blanco.
        """
        super().__init__(**kwargs)
        self.current_color = (0, 0, 0, 1)   # Negro por defecto (RGBA)
        self._set_background()
        logger.info("DrawingArea inicializada.")

    # ------------------------------------------------------------------ #
    #   API que usará pantalla_dibujo.py
    # ------------------------------------------------------------------ #
    def set_color(self, rgba: tuple[float, float, float, float]):
        """
        Cambia el color de dibujo para los trazos futuros.

        :param rgba: Una tupla de 4 floats (R, G, B, A) donde cada valor está en el rango [0, 1].
        """
        self.current_color = rgba
        logger.debug(f"Color de dibujo cambiado a: {rgba}")

    def clear_canvas(self):
        """
        Borra todo el contenido del lienzo y restablece el fondo blanco.
        """
        self.canvas.clear()
        self._set_background()
        logger.info("Lienzo borrado.")

    def export_to_png(self, filepath: str, crop: bool = False) -> str:
        """
        Exporta el contenido del DrawingArea a un archivo PNG.

        :param filepath: La ruta completa del archivo donde se guardará el PNG.
        :param crop: Si es True, intenta recortar el área dibujada (no implementado en esta versión simple).
        :return: La misma ruta del archivo si la exportación fue exitosa, o una cadena vacía en caso de error.
        """
        try:
            if self.size[0] == 0 or self.size[1] == 0:
                logger.warning("DrawingArea tiene tamaño cero. No se puede exportar.")
                return ""

            img = self.export_as_image()
            img.save(filepath)
            logger.info(f"Dibujo exportado a: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error al exportar dibujo a PNG: {e}")
            return ""

    # ------------------------------------------------------------------ #
    #   Events
    # ------------------------------------------------------------------ #
    def on_touch_down(self, touch):
        """
        Maneja el evento de 'tocar hacia abajo' en el lienzo.

        Si el toque está dentro del área de dibujo, inicia una nueva línea
        con el color actual y almacena la línea en `touch.ud`.

        :param touch: Objeto Touch que contiene la posición y otras propiedades del toque.
        :return: True si el toque fue manejado por este widget, False en caso contrario.
        """
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.current_color)
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=dp(2))
            logger.debug(f"Toque inicial en: ({touch.x}, {touch.y})")
            return True
        return False

    def on_touch_move(self, touch):
        """
        Maneja el evento de 'mover el toque' en el lienzo.

        Si el toque está dentro del área de dibujo y una línea fue iniciada
        previamente por este toque, añade la nueva posición a la línea.

        :param touch: Objeto Touch que contiene la posición y otras propiedades del toque.
        :return: True si el toque fue manejado por este widget, False en caso contrario.
        """
        if self.collide_point(*touch.pos) and "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]
            logger.debug(f"Toque movido a: ({touch.x}, {touch.y})")
            return True
        return False

    # ------------------------------------------------------------------ #
    def _set_background(self):
        """
        Establece el color de fondo del lienzo a blanco.
        """
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=partial(self._update_bg_rect, self.bg_rect),
                  size=partial(self._update_bg_rect, self.bg_rect))
        logger.debug("Fondo del lienzo establecido.")

    def _update_bg_rect(self, rect_instance, instance, value):
        """Actualiza la posición y tamaño del rectángulo de fondo."""
        rect_instance.pos = instance.pos
        rect_instance.size = instance.size

Factory.register(classname='DrawingArea', module='componentes')
