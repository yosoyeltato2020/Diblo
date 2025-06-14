from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from componentes import DrawingArea
from palabras import Palabras
from pronunciador import reproducir_palabra
from reconocimiento_offline import reconocer_voz
from kivy.graphics import Color, Rectangle  # fondo opcional


class DibujoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # ------- etiqueta visible -------
        self.lbl_palabra = Label(
            markup=True,
            font_size='28sp',
            size_hint_y=None,        # altura fija
            halign='center',
            valign='middle'
        )
        # altura según el alto del texto
        self.lbl_palabra.bind(texture_size=lambda l, t: setattr(l, 'height', t[1] + 20))

        # fondo gris clarito para que se vea
        with self.lbl_palabra.canvas.before:
            Color(0.7, 0.85, 1, 1)
            self.bg = Rectangle()
        self.lbl_palabra.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(self.lbl_palabra)
        # --------------------------------

        # resto igual que antes …
        self.area_dibujo = DrawingArea(size_hint=(1, 0.7))
        self.add_widget(self.area_dibujo)

        botones = BoxLayout(size_hint_y=0.2)
        for txt, fn in [
            ("Cambiar palabra", self.cambiar_palabra),
            ("Borrar", self.borrar_dibujo),
            ("Pronunciar", self.pronunciar),
            ("Hablar", self.reconocer)
        ]:
            b = Button(text=txt); b.bind(on_press=fn); botones.add_widget(b)
        self.add_widget(botones)

        self.palabras = Palabras()
        self.palabra_actual = ''
        self.cambiar_palabra()            # primera palabra

    # ---- util para fondo de la etiqueta ----
    def _update_bg(self, *args):
        self.bg.pos = self.lbl_palabra.pos
        self.bg.size = self.lbl_palabra.size
    # ----------------------------------------

    def cambiar_palabra(self, *a):
        self.palabra_actual = self.palabras.nueva_palabra()
        self.lbl_palabra.text = f"[b]Dibuja: {self.palabra_actual.upper()}[/b]"
        self.area_dibujo.borrar_canvas()
        reproducir_palabra(self.palabra_actual)

    def borrar_dibujo(self, *_):  self.area_dibujo.borrar_canvas()
    def pronunciar(self, *_):      reproducir_palabra(self.palabra_actual)

    def reconocer(self, *_):
        texto = reconocer_voz()
        if texto:
            self.lbl_palabra.text = f"[color=00aa00]Has dicho:[/color] {texto}"
        else:
            self.lbl_palabra.text = "[color=ff0000]No se entendió[/color]"
