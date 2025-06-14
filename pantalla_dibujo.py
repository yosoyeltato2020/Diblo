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
    """Widget principal con palabra, lienzo, botones y feedback de voz."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # ── Etiqueta superior ────────────────────────────────────────────
        self.lbl_palabra = Label(
            markup=True,
            font_size="28sp",
            size_hint_y=None,
            halign="center",
            valign="middle",
        )
        self.lbl_palabra.bind(
            texture_size=lambda l, t: setattr(l, "height", t[1] + 20)
        )
        with self.lbl_palabra.canvas.before:
            Color(0.7, 0.85, 1, 1)
            self._bg = Rectangle()
        self.lbl_palabra.bind(pos=self._update_bg, size=self._update_bg)
        self.add_widget(self.lbl_palabra)

        # ── Área de dibujo ───────────────────────────────────────────────
        self.area_dibujo = DrawingArea(size_hint=(1, 0.7))
        self.add_widget(self.area_dibujo)

        # ── Barra de botones ─────────────────────────────────────────────
        barra = BoxLayout(size_hint_y=0.2)
        for texto, cb in [
            ("Cambiar palabra", self.cambiar_palabra),
            ("Borrar", self.borrar_dibujo),
            ("Pronunciar", self.pronunciar),
            ("Hablar", self.reconocer),
        ]:
            btn = Button(text=texto)
            btn.bind(on_press=cb)
            barra.add_widget(btn)
        self.add_widget(barra)

        # ── Lógica de palabras ───────────────────────────────────────────
        self.palabras = Palabras()
        self.palabra_actual = ""
        self._recognizing = False

    # ---------------------------------------------------------------------
    def _update_bg(self, *_):
        self._bg.pos = self.lbl_palabra.pos
        self._bg.size = self.lbl_palabra.size

    # ----------------- Acciones de botones --------------------------------
    def cambiar_palabra(self, *_):
        """Escoge nueva palabra, actualiza la GUI y pronuncia tras un tick."""
        self.palabra_actual = self.palabras.nueva_palabra()
        self.lbl_palabra.text = f"[b]Dibuja: {self.palabra_actual.upper()}[/b]"
        self.area_dibujo.borrar_canvas()

        # Deja que la GUI se pinte primero → luego reproduce la palabra
        Clock.schedule_once(
            lambda dt: reproducir_palabra(self.palabra_actual), 0
        )

    def borrar_dibujo(self, *_):
        self.area_dibujo.borrar_canvas()

    def pronunciar(self, *_):
        if self.palabra_actual:
            reproducir_palabra(self.palabra_actual)

    # ------------------ Reconocimiento de voz -----------------------------
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
            if texto.strip().lower() == self.palabra_actual.lower():
                self.lbl_palabra.text = (
                    f"[color=00aa00]¡Correcto![/color]\\nHas dicho: {texto}"
                )
            else:
                self.lbl_palabra.text = (
                    f"[color=ff0000]Repítelo otra vez[/color]\\nHas dicho: {texto}"
                )
        else:
            self.lbl_palabra.text = "[color=ff0000]No se entendió[/color]"
        self._recognizing = False
