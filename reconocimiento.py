import speech_recognition as sr
import socket

def hay_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

if not hay_internet():
    from vosk import Model, KaldiRecognizer
    import json
    import os

    MODELO_VOSK = os.path.expanduser("~/vosk-models/vosk-model-small-es-0.42")
    if not os.path.exists(MODELO_VOSK):
        raise RuntimeError("Modelo de Vosk no encontrado en " + MODELO_VOSK)
    model = Model(MODELO_VOSK)

def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5)
            if hay_internet():
                texto = recognizer.recognize_google(audio, language="es-ES")
                return texto
            else:
                rec = KaldiRecognizer(model, 16000)
                rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
                resultado = json.loads(rec.Result())
                return resultado.get("text", "")
        except:
            return None
