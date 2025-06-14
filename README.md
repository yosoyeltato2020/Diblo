# Diblo 🖍️🗣️

**Diblo** es una aplicación educativa infantil que ayuda a los niños a **aprender vocabulario mediante el dibujo y la pronunciación**.

---

## 🎯 ¿Qué hace Diblo?

- Muestra una **palabra aleatoria** (como "gato", "sol", "casa").
- El niño puede **dibujarla libremente** en un lienzo interactivo.
- Puede pulsar un botón para **escuchar cómo se pronuncia**.
- Luego puede **repetirla en voz alta**: la app escucha su voz y muestra lo que entendió.
- Incluye un botón para **borrar el dibujo** y comenzar de nuevo.
- Puedes cambiar a una **nueva palabra en cualquier momento**.

---

## 🖼️ Pantalla principal

- Área de dibujo (canvas)
- Palabra mostrada en grande
- Botones:
  - 🎲 Nueva palabra
  - 🔊 Escuchar palabra
  - 🎤 Repetir palabra
  - 🧼 Borrar dibujo

---

## 🛠️ Requisitos

- Python 3
- Librerías:

```bash
pip install kivy gtts SpeechRecognition pyaudio
```

En Linux:

```bash
sudo apt install portaudio19-dev
```

---

## 🚀 Cómo ejecutar

```bash
python main.py
```

---

## 💡 Ideas futuras con IA

- **Reconocimiento de dibujos** con redes neuronales (por ejemplo, usando el dataset QuickDraw de Google).
- **Validación automática del dibujo**: comparar lo que el niño dibuja con la palabra objetivo.
- **Detección de pronunciación correcta** y mejora de acentos.
- **Sistema de recompensas o estrellas** por cada palabra pronunciada correctamente.
- **Modo multilingüe**: enseñar palabras en varios idiomas (español, inglés, francés...).
- **Modo historia**: las palabras dibujadas se usan para contar un cuento generado por IA.
- **Exportar dibujos** o progresos a PDF o galería.

---

## 👨‍👧 Público objetivo

- Niños de 4 a 9 años
- Padres y educadores que buscan herramientas lúdicas para el aprendizaje de idiomas

---

## 📦 Estructura del proyecto

```
Diblo/
├── main.py
├── pantalla_dibujo.py
├── componentes.py
├── pronunciador.py
├── reconocimiento.py
├── palabras.py
└── README.md
```

---

## ❤️ Autor

Este proyecto fue creado como prototipo educativo. Se puede extender libremente.
