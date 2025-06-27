# config.py
"""
Archivo de configuración centralizada para la aplicación Diblo.
Contiene constantes y valores configurables para colores, rutas,
tiempos, y otras propiedades de la interfaz de usuario.
"""

# --- Configuración de Colores (RGBA: R, G, B, A; cada valor en [0, 1]) ---
# Paleta de colores para el área de dibujo
PALETA_COLORES = [
    (0, 0, 0, 1),       # Negro
    (1, 0, 0, 1),       # Rojo
    (0, 0.6, 0, 1),     # Verde oscuro
    (0, 0.5, 1, 1),     # Azul brillante
    (1, 0.7, 0, 1),     # Naranja
    (0.6, 0, 0.8, 1),   # Morado
]

# Color de fondo de la etiqueta de la palabra a dibujar
COLOR_FONDO_ETIQUETA = (0.7, 0.85, 1, 1) # Azul claro pastel

# Colores para mensajes de reconocimiento de voz
COLOR_ESCUCHANDO = (1, 0.66, 0, 1)   # Naranja para "Escuchando..."
COLOR_CORRECTO = (0, 0.66, 0, 1)     # Verde para "¡Correcto!"
COLOR_ERROR = (1, 0, 0, 1)          # Rojo para "No se entendió" o errores

# Colores para botones en Popups
COLOR_BOTON_PRIMARIO = (0.3, 0.6, 1, 1) # Azul general
COLOR_BOTON_ACEPTAR = (0.2, 0.7, 0.2, 1) # Verde para "Sí"
COLOR_BOTON_CANCELAR = (0.7, 0.2, 0.2, 1) # Rojo para "No"

# --- Configuración de Rutas y Modelos ---
# Ruta al modelo de Vosk (para reconocimiento offline de voz)
# El modelo se espera dentro de la carpeta 'vosk_model/' en el directorio del proyecto.
RUTA_MODELO_VOSK = "vosk_model/vosk-model-small-es-0.42"

# Rutas a los efectos de sonido
# Debes tener estos archivos .mp3 o .wav en la carpeta 'audio/'
SONIDO_INICIO_GRABACION = "audio/grabacion_inicio.mp3" # <-- Asegúrate de que sea .mp3 o .wav según tu archivo
SONIDO_FIN_GRABACION = "audio/grabacion_fin.mp3"       # <-- Asegúrate de que sea .mp3 o .wav según tu archivo

# --- Configuración de Audio para Reconocimiento ---
# Tasa de muestreo de audio para el reconocimiento de voz (en Hz)
AUDIO_SAMPLE_RATE = 16000
# Duración máxima de espera para la detección de voz (en segundos)
AUDIO_TIMEOUT_SECS = 5
# Duración de la calibración de ruido ambiental al inicio del reconocimiento (en segundos)
AUDIO_CALIBRATION_SECS = 1

# --- Configuración de Red ---
# Tiempo de espera para la comprobación de conexión a internet (en segundos)
INTERNET_CHECK_TIMEOUT_SECS = 3

# --- Configuración de Caché ---
# Tamaño máximo de la caché LRU para audios de gTTS (número de palabras)
CACHELRU_MAX_SIZE = 128

# --- Dimensiones y Espaciados de UI ---
ESPACIADO_BOTONES = 10 # Espaciado entre botones en la botonera
ANCHO_SPINNER_CATEGORIAS = 150 # Ancho fijo para el Spinner de categorías

# Popups generales
ESPACIADO_POPUP = 10
ALTURA_BOTON_POPUP = 40

# Popups de Confirmación (ej. Borrar Dibujo)
ANCHO_POPUP_CONFIRMACION = 0.7 # 70% del ancho de la ventana
ALTO_POPUP_CONFIRMACION = 0.3 # 30% del alto de la ventana

# Popups de Problemas de Reconocimiento
ANCHO_POPUP_PROBLEMA = 0.8
ALTO_POPUP_PROBLEMA = 0.4
ALTO_POPUP_PROBLEMA_PEQ = 0.3 # Para mensajes más cortos

# Popups de Guardar Dibujo
ANCHO_POPUP_GUARDAR_DIBUJO = 0.8
ALTO_POPUP_GUARDAR_DIBUJO = 0.8 # Más alto para mostrar la imagen