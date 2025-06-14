from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from componentes import DrawingArea
from palabras import Palabras
from pronunciador import reproducir_palabra
from reconocimiento_offline import reconocer_voz
from kivy.graphics import Color, Rectangle

class DibujoWidget(BoxLayout):
    """Widget principal que combina etiqueta, área de dibujo y cuatro botones."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # ── Etiqueta con la palabra ───────────────────────────
        self.lbl_palabra = Label(
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            halign='center',
            valign='middle'
        )
        # Altura dinámica según el texto
        self.lbl_palabra.bind(texture_size=lambda l, t: setattr(l, 'height', t[1] + 20))

        # Fondo azul claro detrás de la etiqueta
        with self.lbl_palabra.canvas.before:
            Color(0.7, 0.85, 1, 1)
            self._bg = Rectangle()
        self.lbl_palabra.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(self.lbl_palabra)

        # ── Área de dibujo ────────────────────────────────────
        self.area_dibujo = DrawingArea(size_hint=(1, 0.7))
        self.add_widget(self.area_dibujo)

        # ── Botones ───────────────────────────────────────────
        barra_botones = BoxLayout(size_hint_y=0.2)
        for texto, callback in [
            ("Cambiar palabra", self.cambiar_palabra),
            ("Borrar", self.borrar_dibujo),
            ("Pronunciar", self.pronunciar),
            ("Hablar", self.reconocer),
        ]:
            btn = Button(text=texto)
            btn.bind(on_press=callback)
            barra_botones.add_widget(btn)
        self.add_widget(barra_botones)

        # ── Lógica de palabras ────────────────────────────────
        self.palabras = Palabras()
        self.palabra_actual = ''  # se establecerá al entrar en la pantalla

    # ---------------------------------------------------------
    def _update_bg(self, *_):
        self._bg.pos = self.lbl_palabra.pos
        self._bg.size = self.lbl_palabra.size

    def cambiar_palabra(self, *_):
        self.palabra_actual = self.palabras.nueva_palabra()
        self.lbl_palabra.text = f"[b]Dibuja: {self.palabra_actual.upper()}[/b]"
        self.area_dibujo.borrar_canvas()
        reproducir_palabra(self.palabra_actual)

    def borrar_dibujo(self, *_):
        self.area_dibujo.borrar_canvas()

    def pronunciar(self, *_):
        if self.palabra_actual:
            reproducir_palabra(self.palabra_actual)

    def reconocer(self, *_):
        texto = reconocer_voz()
        if texto:
            self.lbl_palabra.text = f"[color=00aa00]Has dicho:[/color] {texto}"
        else:
            self.lbl_palabra.text = "[color=ff0000]No se entendió[/color]"
