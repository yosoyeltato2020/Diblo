# palabras.py
import random
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Palabras:
    """
    Gestiona la lista de palabras para el juego de dibujo.
    Carga las palabras desde un archivo JSON, soporta categorías
    y permite seleccionar una nueva palabra aleatoria.
    """

    def __init__(self, filepath: Path = Path("palabras.json")):
        """
        Inicializa el gestor de palabras.

        :param filepath: La ruta al archivo JSON que contiene las palabras.
                         Por defecto, busca 'palabras.json' en la misma carpeta.
        """
        self.filepath = filepath
        self.data = self._cargar_palabras()
        self.categorias = list(self.data.get("categorias", {}).keys()) # Obtener categorías de forma segura
        self.current_category = None # La categoría actualmente seleccionada
        self.lista_actual = []       # La lista de palabras activa para la selección
        self._set_default_list()
        logger.info(f"Gestor de palabras inicializado. Categorías disponibles: {self.categorias}")

    def _cargar_palabras(self) -> dict:
        """
        Carga las palabras desde el archivo JSON especificado.
        Si el archivo no existe o hay un error, devuelve datos por defecto.

        :return: Un diccionario con las palabras cargadas o los datos por defecto.
        """
        if not self.filepath.exists():
            logger.warning(f"Archivo de palabras no encontrado en {self.filepath}. Usando lista por defecto.")
            return self._generar_default_data()
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Palabras cargadas desde {self.filepath}.")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Error al leer JSON de palabras desde {self.filepath}: {e}. Usando lista por defecto.")
            return self._generar_default_data()
        except Exception as e:
            logger.error(f"Error inesperado al cargar palabras desde {self.filepath}: {e}. Usando lista por defecto.")
            return self._generar_default_data()

    def _generar_default_data(self) -> dict:
        """
        Crea una estructura de datos por defecto para las palabras si no se puede cargar el archivo.

        :return: Un diccionario con categorías y una lista por defecto.
        """
        default_words = ["sol", "luna", "casa", "gato", "perro",
                         "árbol", "flor", "nube", "estrella", "mar"]
        return {
            "categorias": {
                "Defecto": default_words # Renombrado a "Defecto" para ser más amigable
            },
            "default": default_words
        }

    def _set_default_list(self):
        """
        Establece la lista de palabras activa a la lista 'default' o
        la primera categoría si 'default' no existe o está vacía.
        """
        if "default" in self.data and self.data["default"]:
            self.lista_actual = self.data["default"]
            self.current_category = None # No hay categoría específica seleccionada, es la lista global
            logger.info("Lista de palabras inicial establecida a la lista 'default'.")
        elif self.categorias:
            self.current_category = self.categorias[0]
            self.lista_actual = self.data["categorias"][self.current_category]
            logger.info(f"Lista de palabras inicial establecida a la primera categoría: {self.current_category}.")
        else:
            self.lista_actual = []
            logger.warning("No hay palabras en la lista 'default' ni en ninguna categoría. La lista actual está vacía.")


    def nueva_palabra(self) -> str:
        """
        Selecciona y devuelve una nueva palabra aleatoria de la lista activa.

        :return: Una palabra aleatoria, o una cadena vacía si la lista está vacía.
        """
        if not self.lista_actual:
            logger.warning("No hay palabras en la lista actual. Devolviendo cadena vacía.")
            return ""
        palabra = random.choice(self.lista_actual)
        logger.debug(f"Nueva palabra seleccionada: {palabra}")
        return palabra

    def get_categorias(self) -> list[str]:
        """
        Devuelve una lista de los nombres de las categorías de palabras disponibles.

        :return: Una lista de strings con los nombres de las categorías.
        """
        # Asegurarse de que las categorías estén actualizadas si se añaden/eliminan dinámicamente
        self.categorias = list(self.data.get("categorias", {}).keys())
        return self.categorias

    def set_categoria(self, categoria: str) -> bool:
        """
        Cambia la lista de palabras activa a una categoría específica.

        :param categoria: El nombre de la categoría a activar.
        :return: True si la categoría se estableció con éxito, False en caso contrario.
        """
        if categoria in self.data.get("categorias", {}):
            self.current_category = categoria
            self.lista_actual = self.data["categorias"][categoria]
            logger.info(f"Cambiando a categoría: '{categoria}'. Palabras: {self.lista_actual}")
            return True
        logger.warning(f"Categoría '{categoria}' no encontrada.")
        return False

    def get_current_category(self) -> str | None:
        """
        Devuelve el nombre de la categoría de palabras actualmente activa.

        :return: El nombre de la categoría como string, o None si no hay una categoría activa.
        """
        return self.current_category

    def get_current_words(self) -> list[str]:
        """
        Devuelve la lista de palabras actualmente activa.

        :return: Una lista de strings con las palabras de la categoría o lista por defecto actual.
        """
        return self.lista_actual

    def add_word_to_category(self, word: str, category: str) -> bool:
        """
        Añade una palabra a una categoría específica y guarda los cambios en el archivo.

        :param word: La palabra a añadir.
        :param category: La categoría a la que añadir la palabra.
        :return: True si la palabra fue añadida (o ya existía), False si hubo un error al guardar.
        """
        word = word.strip().lower() # Normalizar la palabra
        if not word:
            logger.warning("Intento de añadir una palabra vacía.")
            return False

        if category not in self.data["categorias"]:
            self.data["categorias"][category] = []
            self.categorias = list(self.data["categorias"].keys()) # Actualizar lista de categorías
            logger.info(f"Nueva categoría '{category}' creada.")

        if word not in self.data["categorias"][category]:
            self.data["categorias"][category].append(word)
            logger.info(f"Palabra '{word}' añadida a la categoría '{category}'.")
            if self._guardar_palabras():
                # Si la categoría añadida es la actual, actualiza la lista activa
                if self.current_category == category:
                    self.lista_actual = self.data["categorias"][category]
                return True
            return False # Falló al guardar
        logger.info(f"Palabra '{word}' ya existe en la categoría '{category}'.")
        return True # Ya existía, se considera "éxito"


    def remove_word_from_category(self, word: str, category: str) -> bool:
        """
        Elimina una palabra de una categoría específica y guarda los cambios.

        :param word: La palabra a eliminar.
        :param category: La categoría de la que eliminar la palabra.
        :return: True si la palabra fue eliminada, False si no se encontró o hubo un error al guardar.
        """
        word = word.strip().lower() # Normalizar
        if category in self.data.get("categorias", {}) and word in self.data["categorias"][category]:
            self.data["categorias"][category].remove(word)
            logger.info(f"Palabra '{word}' eliminada de la categoría '{category}'.")
            if not self.data["categorias"][category]: # Si la categoría se queda vacía, la puedes eliminar (opcional)
                del self.data["categorias"][category]
                self.categorias = list(self.data["categorias"].keys())
                logger.info(f"Categoría '{category}' eliminada por estar vacía.")
                # Si la categoría eliminada era la actual, vuelve a la lista por defecto
                if self.current_category == category:
                    self._set_default_list()

            if self._guardar_palabras():
                # Actualiza la lista activa si la palabra estaba en la categoría actual
                if self.current_category == category:
                    self.lista_actual = self.data["categorias"].get(category, []) # Puede que la categoría se haya borrado
                return True
            return False # Falló al guardar
        logger.warning(f"Palabra '{word}' no encontrada en la categoría '{category}' para eliminar.")
        return False

    def _guardar_palabras(self) -> bool:
        """
        Guarda el estado actual de las palabras y categorías en el archivo JSON.

        :return: True si se guardó con éxito, False en caso de error.
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logger.info(f"Palabras guardadas en {self.filepath}.")
            return True
        except Exception as e:
            logger.error(f"Error al guardar palabras en {self.filepath}: {e}")
            return False