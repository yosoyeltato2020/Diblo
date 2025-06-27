from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


class DrawingArea(Widget):
    """Lienzo donde el usuario dibuja con el color actual."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_color = (0, 0, 0, 1)   # negro por defecto
        self._set_background()

    # ------------------------------------------------------------------ #
    #   API que usará pantalla_dibujo.py
    # ------------------------------------------------------------------ #
    def set_color(self, rgba):
        """Cambia el color con el que se dibujarán los siguientes trazos."""
        self.current_color = rgba

    def borrar_canvas(self):
        self.canvas.clear()
        self._set_background()

    # ------------------------------------------------------------------ #
    #   Events
    # ------------------------------------------------------------------ #
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.current_color)
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=2)
            return True
        return False

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]
            return True
        return False

    # ------------------------------------------------------------------ #
    def _set_background(self):
        with self.canvas:
            Color(1, 1, 1, 1)   # blanco
