import speech_recognition as sr
import socket
import os
import json
import logging

try:
    from vosk import Model, KaldiRecognizer
except ImportError:
    Model = None
    KaldiRecognizer = None

import config

logger = logging.getLogger(__name__)


def hay_internet():
    """Devuelve True si hay conexión a Internet."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=config.INTERNET_CHECK_TIMEOUT_SECS)
        return True
    except OSError:
        return False


# Cargar el modelo Vosk solo si está disponible y se necesita
modelo_vosk = None
if not hay_internet() and KaldiRecognizer:
    if os.path.exists(config.RUTA_MODELO_VOSK):
        modelo_vosk = Model(config.RUTA_MODELO_VOSK)
    else:
        logger.warning(f"Modelo Vosk no encontrado en: {config.RUTA_MODELO_VOSK}")


def reconocer_voz():
    """
    Reconoce la voz del usuario usando Google (online) o Vosk (offline) según disponibilidad.
    :return: Texto reconocido o None si hubo error.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=config.AUDIO_CALIBRATION_SECS)
            audio = recognizer.listen(source, timeout=config.AUDIO_TIMEOUT_SECS)

            if hay_internet():
                texto = recognizer.recognize_google(audio, language="es-ES")
                logger.info(f"[ONLINE] Reconocido: {texto}")
                return texto

            elif modelo_vosk and KaldiRecognizer:
                rec = KaldiRecognizer(modelo_vosk, config.AUDIO_SAMPLE_RATE)
                rec.AcceptWaveform(audio.get_raw_data(
                    convert_rate=config.AUDIO_SAMPLE_RATE,
                    convert_width=2
                ))
                resultado = json.loads(rec.Result())
                texto = resultado.get("text", "")
                logger.info(f"[OFFLINE] Reconocido: {texto}")
                return texto

            else:
                logger.warning("Reconocimiento offline no disponible.")
                return None

        except sr.WaitTimeoutError:
            logger.warning("Tiempo de espera agotado esperando voz.")
        except sr.UnknownValueError:
            logger.info("No se entendió lo que se dijo.")
        except Exception as e:
            logger.error(f"Error en reconocimiento de voz: {e}")

    return None
