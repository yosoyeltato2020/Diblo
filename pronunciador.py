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
import logging

from gtts import gTTS
from playsound import playsound, PlaysoundException # Importar PlaysoundException
import config # Importar la configuración para el tamaño de la caché y rutas de sonido

logger = logging.getLogger(__name__)

# Almacena las rutas generadas para poder borrarlas luego
_cache_paths: set[Path] = set()


@lru_cache(maxsize=config.CACHELRU_MAX_SIZE)
def _audio_file(texto: str) -> Path:
    """
    Devuelve la ruta a un MP3 de la palabra. Lo crea y lo guarda en caché la 1ª vez.

    Utiliza gTTS para sintetizar la voz.

    :param texto: La palabra o frase a sintetizar.
    :return: Un objeto Path a la ruta del archivo MP3 temporal.
    """
    tmp = NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close() # Cierra el manejador de archivo para que gTTS pueda escribir

    try:
        gTTS(text=texto, lang="es").save(tmp.name)
        file_path = Path(tmp.name)
        _cache_paths.add(file_path)
        logger.debug(f"Audio generado y cacheado para '{texto}': {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error al generar audio para '{texto}': {e}")
        # Intentar limpiar el archivo temporal creado si la síntesis falla
        if Path(tmp.name).exists():
            try:
                Path(tmp.name).unlink()
                logger.debug(f"Archivo temporal '{tmp.name}' eliminado tras error de síntesis.")
            except OSError as ex:
                logger.warning(f"No se pudo eliminar archivo temporal '{tmp.name}' tras error de síntesis: {ex}")
        raise # Re-lanzar la excepción para que el llamador la maneje


def _play_sound_effect(sound_path: Path):
    """
    Reproduce un efecto de sonido sin bloquear el hilo principal.

    :param sound_path: Objeto Path a la ruta del archivo de sonido.
    """
    if not sound_path.exists():
        logger.warning(f"Archivo de sonido no encontrado: {sound_path}")
        return

    try:
        playsound(str(sound_path), block=False) # playsound a veces prefiere string
        logger.debug(f"Efecto de sonido reproducido: {sound_path}")
    except PlaysoundException as e:
        logger.error(f"Error reproduciendo efecto de sonido '{sound_path}': {e}")
    except Exception as e:
        logger.error(f"Error inesperado al reproducir sonido '{sound_path}': {e}")


def reproducir_palabra(texto: str) -> None:
    """
    Reproduce la palabra proporcionada sin bloquear la GUI.
    Cada llamada se lanza en su propio hilo.

    :param texto: La palabra a reproducir.
    """
    def _worker():
        try:
            path = _audio_file(texto.lower()) # Asegura minúsculas para la caché y gTTS
            _play_sound_effect(path)
        except Exception as e:
            logger.error(f"Error en hilo de reproducción de palabra '{texto}': {e}")

    threading.Thread(target=_worker, daemon=True).start()
    logger.info(f"Reproducción de palabra '{texto}' lanzada en hilo.")


def reproducir_inicio_grabacion():
    """Reproduce el sonido de inicio de la grabación de voz."""
    _play_sound_effect(Path(config.SONIDO_INICIO_GRABACION))
    logger.debug("Reproduciendo sonido de inicio de grabación.")

def reproducir_fin_grabacion():
    """Reproduce el sonido de fin de la grabación de voz."""
    _play_sound_effect(Path(config.SONIDO_FIN_GRABACION))
    logger.debug("Reproduciendo sonido de fin de grabación.")


def clear_cache() -> None:
    """
    Elimina todos los MP3 temporales generados por gTTS y limpia la caché LRU.
    """
    global _cache_paths
    logger.info("Iniciando limpieza de caché de audios.")
    files_to_remove = list(_cache_paths) # Copia la lista para iterar

    for path in files_to_remove:
        if path.exists():
            try:
                path.unlink() # Elimina el archivo
                logger.debug(f"Archivo temporal de audio eliminado: {path}")
            except OSError as e:
                logger.warning(f"No se pudo eliminar archivo temporal '{path}': {e}")
        else:
            logger.debug(f"Archivo temporal '{path}' no existe, no necesita ser eliminado.")

    _cache_paths.clear() # Vacía el set de paths registrados
    _audio_file.cache_clear() # Limpia la caché LRU de la función _audio_file
    logger.info("Caché de audios limpiada completamente.")