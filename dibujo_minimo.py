from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

class DibujoWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(0, 0, 0)  # Negro
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=2)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]

class DibujoApp(App):
    def build(self):
        return DibujoWidget()

if __name__ == "__main__":
    DibujoApp().run()
