import json
import logging
from pathlib import Path
from kivy.event import EventDispatcher
from kivy.properties import StringProperty

logger = logging.getLogger(__name__)

class LocaleManager(EventDispatcher):
    """
    Gestor de internacionalización (i18n) para cargar textos en diferentes idiomas.
    Implementa el patrón Singleton para asegurar una única instancia.
    """
    _instance = None
    _texts: dict[str, str] = {} # Diccionario para almacenar los textos cargados
    current_lang = StringProperty("es") # Idioma por defecto

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocaleManager, cls).__new__(cls)
            cls._instance._texts = {}
            cls._instance.register_event_type('on_lang_change') # Registrar el tipo de evento
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, '_initialized'):
            super().__init__(**kwargs)
            self._load_language("es")
            self._load_language("en")
            self.current_lang = "es"
            self._initialized = True

    def on_lang_change(self, *args):
        logger.debug(f"Evento on_lang_change disparado. Nuevo idioma: {self.current_lang}")

    def _load_language(self, lang_code: str):
        current_dir = Path(__file__).parent
        lang_file = current_dir / "lang" / f"{lang_code}.json"

        if not lang_file.exists():
            logger.error(f"Archivo de idioma '{lang_file}' no encontrado.")
            if lang_code not in self._texts:
                self._texts[lang_code] = {}
            return

        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self._texts[lang_code] = json.load(f)
            logger.info(f"Idioma '{lang_code}' cargado exitosamente desde '{lang_file}'.")
        except json.JSONDecodeError as e:
            logger.error(f"Error al leer JSON de idioma '{lang_file}': {e}. Los textos para '{lang_code}' estarán vacíos.")
            self._texts[lang_code] = {}
        except Exception as e:
            logger.error(f"Error inesperado al cargar idioma '{lang_file}': {e}. Los textos para '{lang_code}' estarán vacíos.")
            self._texts[lang_code] = {}

    def get_localized_text(self, key: str) -> str:
        lang = str(self.current_lang)   # Siempre forzamos a str para buscar en el diccionario
        text = self._texts.get(lang, {}).get(key, f"MISSING_TEXT:{key}")
        if text == f"MISSING_TEXT:{key}":
            logger.warning(f"Clave de texto '{key}' no encontrada en el idioma '{lang}'.")
        return text

    def set_language(self, lang_code: str):
        if lang_code != str(self.current_lang):
            if lang_code not in self._texts or not self._texts[lang_code]:
                logger.info(f"Idioma '{lang_code}' no cargado, intentando cargar ahora.")
                self._load_language(lang_code)

            if lang_code in self._texts and self._texts[lang_code]:
                logger.info(f"Cambiando idioma a '{lang_code}'.")
                self.current_lang = lang_code
                # StringProperty disparará evento
            else:
                logger.warning(f"No se pudo establecer el idioma a '{lang_code}'. Textos no disponibles.")
        else:
            logger.debug(f"Idioma ya establecido a '{lang_code}'. No se requiere cambio.")

    def get_all_languages(self) -> list[str]:
        return list(self._texts.keys())

    def get_current_lang(self) -> str:
        return str(self.current_lang)   # ¡Siempre str!

locale_manager = LocaleManager()

def _(key: str) -> str:
    return locale_manager.get_localized_text(key)
