import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Directorio donde se guardará la caché de audios
# Puedes ajustarlo según tus necesidades
CACHE_DIR = Path("cache_audios")

def init_cache_dir():
    """
    Crea el directorio de caché si no existe.
    """
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio de caché asegurado: {CACHE_DIR.resolve()}")
    except Exception as e:
        logger.error(f"Error al crear el directorio de caché '{CACHE_DIR}': {e}")

def get_cache_path(filename: str) -> Path:
    """
    Devuelve la ruta completa para un archivo dentro del directorio de caché.
    """
    return CACHE_DIR / filename

def clear_audio_cache():
    """
    Elimina todos los archivos del directorio de caché de audios.
    """
    logger.info("Iniciando limpieza de caché de audios.")
    try:
        if CACHE_DIR.exists() and CACHE_DIR.is_dir():
            for item in CACHE_DIR.iterdir():
                if item.is_file():
                    item.unlink() # Elimina el archivo
                    # logger.debug(f"Archivo de caché eliminado: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item) # Elimina subdirectorios recursivamente
                    # logger.debug(f"Directorio de caché eliminado: {item.name}")
            logger.info("Caché de audios limpiada completamente.")
        else:
            logger.info("El directorio de caché de audios no existe o no es un directorio. No se necesita limpieza.")
    except Exception as e:
        logger.error(f"Error al limpiar la caché de audios: {e}")

# Ejemplo de uso (opcional, para pruebas)
if __name__ == "__main__":
    init_cache_dir()
    test_file = get_cache_path("test_audio.mp3")
    with open(test_file, 'w') as f:
        f.write("Esto es un archivo de prueba.")
    logger.info(f"Archivo de prueba creado en: {test_file.resolve()}")
    clear_audio_cache()
    if not test_file.exists():
        logger.info("El archivo de prueba fue eliminado.")