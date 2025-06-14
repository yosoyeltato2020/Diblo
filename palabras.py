import random

class Palabras:
    def __init__(self):
        self.lista = [
            "sol", "luna", "casa", "gato", "perro",
            "árbol", "flor", "nube", "estrella", "mar"
        ]

    def nueva_palabra(self):
        return random.choice(self.lista)
