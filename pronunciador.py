"""pronunciador.py — gTTS + playsound sin solapamientos

Reproduce la palabra solo si no hay otra locución en curso; evita que se
solapen dos audios cuando el usuario pulsa rápidamente varios botones o si
`cambiar_palabra()` se invoca dos veces por accidente.

* Requiere gTTS y playsound (>=1.3.0).
* No depende de reproductores externos.
"""

from tempfile import NamedTemporaryFile
import threading
import os
from gtts import gTTS
from playsound import playsound  # pip install playsound==1.3.0

# ── Control de concurrencia ────────────────────────────────────────────────
_is_playing = False  # indica si hay un audio sonando
_lock = threading.Lock()


def reproducir_palabra(palabra: str) -> None:
    """Genera un MP3 y lo reproduce solo si no hay otro audio activo."""

    global _is_playing
    with _lock:
        if _is_playing:
            # Ya se está reproduciendo algo; ignoramos la nueva petición
            return
        _is_playing = True

    def _worker():
        try:
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                gTTS(text=palabra, lang="es").save(tmp.name)
                # playsound es bloqueante; cuando termina el audio, devuelve
                playsound(tmp.name)
        finally:
            # Limpiar el archivo temporal y liberar el flag
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
            with _lock:
                global _is_playing
                _is_playing = False

    threading.Thread(target=_worker, daemon=True).start()
