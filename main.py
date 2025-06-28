from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
import logging

import config
import pronunciador
import cache_manager
import locale_manager
from pantalla_dibujo import PantallaDibujo
from palabras import Palabras

logger = logging.getLogger(__name__)


class RootWidget(BoxLayout):
    sm = ObjectProperty(None)


class WelcomeScreen(Screen):
    def on_enter(self):
        logger.info("Pantalla de bienvenida mostrada")


class LanguageScreen(Screen):
    selected_language_name = StringProperty("Español")

    def on_kv_post(self, base_widget):
        locale_manager.locale_manager.bind(on_lang_change=self.update_texts)
        self.update_texts()

        from palabras import Palabras
        gestor = Palabras()
        self.ids.categoria_spinner.values = ["Todas las categorías"] + gestor.get_categorias()

    def update_texts(self, *args):
        if self.ids and "lang_spinner" in self.ids:
            lang_code = locale_manager.locale_manager.get_current_lang()
            self.ids.lang_spinner.text = "Español" if lang_code == "es" else "English"
            self.selected_language_name = self.ids.lang_spinner.text

    def on_lang_spinner_text(self, text):
        if text == "Español":
            locale_manager.locale_manager.set_language("es")
        elif text == "English":
            locale_manager.locale_manager.set_language("en")
        self.selected_language_name = text

    def ir_a_pantalla_dibujo(self):
        categoria = self.ids.categoria_spinner.text
        pantalla_dibujo = self.manager.get_screen("pantalla_dibujo")
        pantalla_dibujo.set_categoria(categoria)
        self.manager.current = "pantalla_dibujo"


class DibloApp(App):
    sm = ObjectProperty(None)

    def build(self):
        self.title = "Diblo"
        return RootWidget()

    def on_start(self):
        self.sm = self.root.ids.screen_manager
        cache_manager.init_cache_dir()
        Clock.schedule_once(self.show_welcome, 0.5)

    def on_stop(self):
        cache_manager.clear_audio_cache()

    def show_welcome(self, dt):
        self.sm.current = "welcome_screen"


if __name__ == "__main__":
    DibloApp().run()
