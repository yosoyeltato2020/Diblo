from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from componentes import DrawingArea
from palabras import Palabras
from pronunciador import reproducir_palabra
from reconocimiento_offline import reconocer_voz

class DibujoWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.palabras = Palabras()
        self.area_dibujo = DrawingArea(size_hint=(1, 0.8))
        self.add_widget(self.area_dibujo)

        self.botonera = BoxLayout(size_hint=(1, 0.2))
        self.add_widget(self.botonera)

        self.boton_cambiar = Button(text="Cambiar palabra")
        self.boton_borrar = Button(text="Borrar")
        self.boton_pronunciar = Button(text="Pronunciar")
        self.boton_voz = Button(text="Repetir voz")

        self.boton_cambiar.bind(on_press=self.cambiar_palabra)
        self.boton_borrar.bind(on_press=self.borrar_dibujo)
        self.boton_pronunciar.bind(on_press=self.pronunciar)
        self.boton_voz.bind(on_press=self.reconocer)

        for boton in [self.boton_cambiar, self.boton_borrar, self.boton_pronunciar, self.boton_voz]:
            self.botonera.add_widget(boton)

        self.palabra_actual = self.palabras.nueva_palabra()
        print(f"Palabra inicial: {self.palabra_actual}")

    def cambiar_palabra(self, instance):
        self.palabra_actual = self.palabras.nueva_palabra()
        print(f"Nueva palabra: {self.palabra_actual}")

    def borrar_dibujo(self, instance):
        self.area_dibujo.borrar_canvas()

    def pronunciar(self, instance):
        reproducir_palabra(self.palabra_actual)

    def reconocer(self, instance):
        texto = reconocer_voz()
        if texto:
            print(f"Reconocido: {texto}")
            if texto.lower() == self.palabra_actual.lower():
                print("¡Correcto!")
            else:
                print("Incorrecto. Intenta de nuevo.")
