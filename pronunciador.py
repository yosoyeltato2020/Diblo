from gtts import gTTS
import os
import tempfile
import threading

def reproducir_palabra(palabra, idioma="es"):
    def speak():
        tts = gTTS(text=palabra, lang=idioma)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            os.system(f"start {fp.name}" if os.name == "nt" else f"xdg-open {fp.name}")
    threading.Thread(target=speak).start()
