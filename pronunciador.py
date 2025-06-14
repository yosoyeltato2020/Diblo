"""
Pronuncia texto con gTTS + playsound.
• Lanza la reproducción en un hilo sin bloquear la interfaz.
• Cachea los MP3 en disco (máx. 128) para no re‑sintetizar palabras.
• clear_cache() borra los ficheros temporales y vacía la caché.
"""

from tempfile import NamedTemporaryFile
from functools import lru_cache
from pathlib import Path
import threading
import os

from gtts import gTTS
from playsound import playsound

# Almacena las rutas generadas para poder borrarlas luego
_cache_paths: set[str] = set()


@lru_cache(maxsize=128)
def _audio_file(texto: str) -> str:
    """Devuelve la ruta a un MP3; lo crea y lo guarda en caché la 1ª vez."""
    tmp = NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()
    gTTS(text=texto, lang="es").save(tmp.name)
    _cache_paths.add(tmp.name)
    return tmp.name


def reproducir_palabra(texto: str) -> None:
    """Reproduce la palabra sin bloquear la GUI (cada llamada en su hilo)."""

    def _worker():
        path = _audio_file(texto.lower())
        playsound(path)

    threading.Thread(target=_worker, daemon=True).start()


def clear_cache() -> None:
    """Elimina los MP3 temporales y limpia la caché LRU."""
    global _cache_paths
    for path in list(_cache_paths):
        if os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass
    _cache_paths.clear()
    _audio_file.cache_clear()
