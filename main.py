import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout  # Importación correcta
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
import logging

import locale_manager
import config
import pronunciador
import reconocimiento_offline
import cache_manager

from pantalla_dibujo import PantallaDibujo
from palabras import Palabras

# --------- RootWidget para vincular con el kv -------------
class RootWidget(BoxLayout):
    sm = ObjectProperty(None)

# --------- WelcomeScreen ---------
class WelcomeScreen(Screen):
    welcome_text = StringProperty("")
    lang_label_text = StringProperty("")
    start_button_text = StringProperty("")
    selected_language_name = StringProperty("Español")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._post_init_binding(), 0)

    def _post_init_binding(self, *args):
        locale_manager.locale_manager.bind(on_lang_change=self.update_ui_text)
        self.update_ui_text()

    def update_ui_text(self, *args):
        self.welcome_text = locale_manager.locale_manager.get_localized_text("welcome_title")
        self.lang_label_text = locale_manager.locale_manager.get_localized_text("language_selection_label")
        self.start_button_text = locale_manager.locale_manager.get_localized_text("start_button")

        if self.ids and 'lang_spinner' in self.ids:
            current_lang_code = locale_manager.locale_manager.get_current_lang()  # CORREGIDO
            if current_lang_code == 'es':
                self.ids.lang_spinner.text = "Español"
            elif current_lang_code == 'en':
                self.ids.lang_spinner.text = "English"

    def on_lang_spinner_text(self, text):
        if text == 'Español':
            locale_manager.locale_manager.set_language('es')
        elif text == 'English':
            locale_manager.locale_manager.set_language('en')
        self.selected_language_name = text

# --------- Aplicación principal ---------
class DibloApp(App):
    sm = ObjectProperty(None)
    palabras_manager = None

    def build(self):
        self.title = "Diblo"
        self.palabras_manager = Palabras()
        # RootWidget se carga automáticamente desde diblo.kv
        pass

    def on_start(self):
        self.root.ids.screen_manager
        self.sm = self.root.ids.screen_manager
        Clock.schedule_once(self.show_main_screen, 0.5)

    def show_main_screen(self, dt):
        self.sm.current = 'welcome_screen'

    def on_stop(self):
        cache_manager.clear_audio_cache()

if __name__ == '__main__':
    cache_manager.init_cache_dir()
    DibloApp().run()
