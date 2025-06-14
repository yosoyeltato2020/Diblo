from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout

class DrawingArea(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(0, 0, 0)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=2)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if 'line' in touch.ud and self.collide_point(*touch.pos):
            touch.ud['line'].points += (touch.x, touch.y)
            return True
        return super().on_touch_move(touch)

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(DrawingArea(size_hint_y=None, height=400))

class PruebaDibujoApp(App):
    def build(self):
        return Root()

if __name__ == '__main__':
    PruebaDibujoApp().run()
