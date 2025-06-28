"""
Archivo de configuración centralizada para la aplicación Diblo.
Contiene constantes y valores configurables para colores, rutas,
tiempos, y otras propiedades de la interfaz de usuario.
"""

# --- 🎨 Paleta de Colores (RGBA: valores en [0, 1]) ---
PALETA_COLORES = [
    (0, 0, 0, 1),       # Negro
    (1, 0, 0, 1),       # Rojo
    (0, 0.6, 0, 1),     # Verde oscuro
    (0, 0.5, 1, 1),     # Azul brillante
    (1, 0.7, 0, 1),     # Naranja
    (0.6, 0, 0.8, 1),   # Morado
    (1, 1, 0, 1),       # Amarillo
    (1, 0.5, 0.8, 1)    # Rosa claro
]

COLOR_FONDO_ETIQUETA = (0.7, 0.85, 1, 1)  # Azul pastel

# --- 🎤 Colores para feedback del reconocimiento de voz ---
COLOR_ESCUCHANDO = (1, 0.66, 0, 1)     # Naranja
COLOR_CORRECTO = (0, 0.66, 0, 1)       # Verde
COLOR_ERROR = (1, 0, 0, 1)             # Rojo

# --- 🧭 Botones para Popups ---
COLOR_BOTON_PRIMARIO = (0.3, 0.6, 1, 1)
COLOR_BOTON_ACEPTAR = (0.2, 0.7, 0.2, 1)
COLOR_BOTON_CANCELAR = (0.7, 0.2, 0.2, 1)

# --- 📁 Rutas de Recursos ---
RUTA_MODELO_VOSK = "vosk_model/vosk-model-small-es-0.42"
SONIDO_INICIO_GRABACION = "audio/grabacion_inicio.mp3"
SONIDO_FIN_GRABACION = "audio/grabacion_fin.mp3"

# --- 🔊 Parámetros de Audio ---
AUDIO_SAMPLE_RATE = 16000
AUDIO_TIMEOUT_SECS = 5
AUDIO_CALIBRATION_SECS = 1

# --- 🌐 Red ---
INTERNET_CHECK_TIMEOUT_SECS = 3

# --- 🧠 Caché de Voz ---
CACHELRU_MAX_SIZE = 128

# --- 📐 UI y Diseño ---
ESPACIADO_BOTONES = 10
ANCHO_SPINNER_CATEGORIAS = 150

# --- 🧱 Popups ---
ESPACIADO_POPUP = 10
ALTURA_BOTON_POPUP = 40

ANCHO_POPUP_CONFIRMACION = 0.7
ALTO_POPUP_CONFIRMACION = 0.3

ANCHO_POPUP_PROBLEMA = 0.8
ALTO_POPUP_PROBLEMA = 0.4
ALTO_POPUP_PROBLEMA_PEQ = 0.3

ANCHO_POPUP_GUARDAR_DIBUJO = 0.8
ALTO_POPUP_GUARDAR_DIBUJO = 0.8
