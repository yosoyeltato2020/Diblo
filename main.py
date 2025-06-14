from kivy.app import App
from pantalla_dibujo import DibujoWidget
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

class DibloApp(App):
    def build(self):
        return DibujoWidget()

if __name__ == '__main__':
    DibloApp().run()
