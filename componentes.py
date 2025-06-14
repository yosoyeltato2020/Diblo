from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

class DrawingArea(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line = None
        self._set_background()

    def _set_background(self):
        with self.canvas:
            Color(1, 1, 1, 1)  # Fondo blanco

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(0, 0, 0, 1)  # Color negro
                self.line = Line(points=[touch.x, touch.y], width=2)
            return True
        return False

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and self.line:
            self.line.points += [touch.x, touch.y]
            return True
        return False

    def borrar_canvas(self):
        self.canvas.clear()
        self._set_background()
