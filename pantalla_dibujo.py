from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import threading

from componentes import DrawingArea
from palabras import Palabras
from pronunciador import reproducir_palabra
from reconocimiento_offline import reconocer_voz


class DibujoWidget(BoxLayout):
    """Widget principal con palabra, lienzo y controles.

    Ahora el usuario ve el color seleccionado porque el botón **Color** cambia
    su propio fondo al tono activo.
    """

    _PALETTE = [
        (0, 0, 0, 1), (1, 0, 0, 1), (0, 0.6, 0, 1),
        (0, 0.5, 1, 1), (1, 0.7, 0, 1), (0.6, 0, 0.8, 1),
    ]

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # ---------- Etiqueta ----------
        self.lbl_palabra = Label(markup=True, font_size="28sp",
                                 size_hint_y=None, halign="center", valign="middle")
        self.lbl_palabra.bind(texture_size=lambda l, t: setattr(l, "height", t[1] + 20))
        with self.lbl_palabra.canvas.before:
            Color(0.7, 0.85, 1, 1)
            self._bg = Rectangle()
        self.lbl_palabra.bind(pos=self._update_bg, size=self._update_bg)
        self.add_widget(self.lbl_palabra)

        # ---------- Lienzo ----------
        self.area_dibujo = DrawingArea(size_hint=(1, 0.7))
        self.add_widget(self.area_dibujo)

        # ---------- Botonera ----------
        barra = BoxLayout(size_hint_y=0.2)
        # Se crea aparte para poder actualizar el color
        self.btn_color = Button(text="Color", background_normal='',
                                background_color=self._PALETTE[0])

        for texto, cb in [
            ("Cambiar palabra", self.cambiar_palabra),
            ("Borrar", self.borrar_dibujo),
            (None, self.cambiar_color),       # placeholder, se añade como btn_color
            ("Pronunciar", self.pronunciar),
            ("Hablar", self.reconocer),
        ]:
            if texto is None:
                self.btn_color.bind(on_press=cb)
                barra.add_widget(self.btn_color)
            else:
                btn = Button(text=texto)
                btn.bind(on_press=cb)
                barra.add_widget(btn)
        self.add_widget(barra)

        # ---------- Estado ----------
        self.palabras = Palabras()
        self.palabra_actual = ""
        self._recognizing = False
        self._color_idx = 0

    # ------------------------------------------------------------------
    def _update_bg(self, *_):
        self._bg.pos, self._bg.size = self.lbl_palabra.pos, self.lbl_palabra.size

    # ---------------- Acciones ----------------------------------------
    def cambiar_palabra(self, *_):
        self.palabra_actual = self.palabras.nueva_palabra()
        self.lbl_palabra.text = f"[b]Dibuja: {self.palabra_actual.upper()}[/b]"
        self.area_dibujo.borrar_canvas()
        Clock.schedule_once(lambda dt: reproducir_palabra(self.palabra_actual), 0)

    def borrar_dibujo(self, *_):
        self.area_dibujo.borrar_canvas()

    def cambiar_color(self, *_):
        self._color_idx = (self._color_idx + 1) % len(self._PALETTE)
        nuevo = self._PALETTE[self._color_idx]
        self.area_dibujo.set_color(nuevo)
        self.btn_color.background_color = nuevo   # feedback visual

    def pronunciar(self, *_):
        if self.palabra_actual:
            reproducir_palabra(self.palabra_actual)

    # ---------------- Reconocimiento de voz ---------------------------
    def reconocer(self, *_):
        if self._recognizing:
            return
        self._recognizing = True
        self.lbl_palabra.text = "[color=ffaa00]Escuchando…[/color]"

        def _worker():
            texto = reconocer_voz()
            Clock.schedule_once(lambda dt: self._procesar_resultado(texto))
        threading.Thread(target=_worker, daemon=True).start()

    def _procesar_resultado(self, texto):
        if texto:
            reproducir_palabra(texto)
            ok = texto.strip().lower() == self.palabra_actual.lower()
            color, msg = ("00aa00", "¡Correcto!") if ok else ("ff0000", "Repítelo otra vez")
            self.lbl_palabra.text = f"[color={color}]{msg}[/color]\\nHas dicho: {texto}"
        else:
            self.lbl_palabra.text = "[color=ff0000]No se entendió[/color]"
        self._recognizing = False
