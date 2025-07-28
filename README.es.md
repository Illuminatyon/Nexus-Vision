# Reconocimiento de Video Python

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![University: Paris 8](https://img.shields.io/badge/University-Paris%208-blue)
![Computer: Vision](https://img.shields.io/badge/Computer-Vision-orange)
![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-red)
![Contributors](https://img.shields.io/badge/Contributors-1-brightgreen)
![Stars](https://img.shields.io/badge/Stars-0-lightgrey)
![Fork](https://img.shields.io/badge/Forks-0-lightgrey)
![Watchers](https://img.shields.io/badge/Watchers-0-lightgrey)

## 🌍 Versiones Multilingües del README

| 🇫🇷 [Français](README.fr.md) | 🇬🇧 [English](README.md) | 🇪🇸 Español (estás aquí) |
|------------------------------|----------------------------|----------------------------|
| [Cambiar a francés](README.fr.md) | [Cambiar a inglés](README.md) | Idioma actual |

## 📘 Descripción General del Proyecto

Este proyecto es una aplicación de visión por computadora que utiliza tu webcam para detectar manos y reconocer expresiones faciales. Las características principales incluyen:

- Detección de manos y conteo de dedos en tiempo real
- Reconocimiento de expresiones faciales (sonrisa, sorpresa, neutral)
- Soporte para ambas manos simultáneamente
- Cálculo de la suma total de dedos extendidos
- Retroalimentación visual con puntuaciones de confianza

La aplicación fue desarrollada para explorar las capacidades de las bibliotecas de visión por computadora y para crear una demostración interactiva de reconocimiento de gestos y expresiones.

## 📊 Características

### Detección de Manos y Conteo de Dedos
- Detecta ambas manos, izquierda y derecha
- Cuenta los dedos extendidos (0-5) en cada mano
- Calcula la suma total de dedos extendidos
- Proporciona retroalimentación visual para los dedos detectados

### Reconocimiento de Expresiones Faciales
- Detecta tres expresiones:
  - Sonrisa: Cuando las comisuras de la boca se elevan
  - Sorpresa: Cuando las cejas se elevan y la boca está abierta
  - Neutral: Expresión predeterminada
- Muestra el porcentaje de confianza para las expresiones detectadas
- Muestra la expresión sobre la cabeza del usuario

## ⚙️ Cómo Funciona

La aplicación utiliza dos tecnologías principales de visión por computadora:

1. **MediaPipe Hands**
   - Detecta puntos de referencia de las manos (21 puntos por mano)
   - Rastrea posiciones y movimientos de los dedos
   - Determina si los dedos están extendidos o doblados

2. **MediaPipe Face Mesh**
   - Detecta puntos de referencia faciales (468 puntos)
   - Rastrea características faciales clave (ojos, cejas, boca)
   - Analiza las posiciones de los puntos de referencia para determinar expresiones

La aplicación procesa cada fotograma de video para:
1. Detectar manos y rostro
2. Analizar posiciones de puntos de referencia
3. Contar dedos extendidos
4. Reconocer expresiones faciales
5. Mostrar resultados con retroalimentación visual

## 🧑‍💻 Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **OpenCV**: Visión por computadora y procesamiento de imágenes
- **MediaPipe**: Frameworks de detección de manos y rostro
- **NumPy**: Cálculos numéricos

## 💻 Instalación

### Requisitos Previos
- Python 3.6 o superior
- Webcam
- Windows, macOS o Linux

### Configuración

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Illuminatyon/video-recognition-python.git
   cd video-recognition-python
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

   O instalar individualmente:
   ```bash
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   ```

3. Verificar instalación:
   ```bash
   python check_libraries.py
   ```

## 📝 Uso

### Ejecutar la Aplicación

```bash
python main.py
```

Para modo de depuración (muestra visualización adicional):
```bash
python main.py --debug
```

### Controles e Interacción

1. **Gestos de Mano**:
   - Muestra tus manos a la cámara
   - Extiende o dobla los dedos para cambiar el conteo
   - Ambas manos pueden ser detectadas simultáneamente

2. **Expresiones Faciales**:
   - Posiciona tu rostro frente a la cámara
   - Sonríe para activar la detección de sonrisa
   - Levanta las cejas y abre la boca para la detección de sorpresa
   - Relaja los músculos faciales para la expresión neutral

3. **Salir**:
   - Presiona 'q' para salir de la aplicación

## 🔍 Solución de Problemas

### Problemas con Bibliotecas

Si encuentras problemas con las bibliotecas:

1. Ejecuta el script de verificación:
   ```bash
   python check_libraries.py
   ```

2. Para problemas con MediaPipe:
   ```bash
   pip install --upgrade mediapipe
   ```

3. Para acceso a la cámara con OpenCV:
   - Asegúrate de que tu webcam esté correctamente conectada
   - Verifica si otras aplicaciones están usando la cámara

### Problemas de Detección

Para una mejor detección de manos:
- Asegura buenas condiciones de iluminación
- Mantén las manos dentro del marco de la cámara
- Posiciona las palmas hacia la cámara
- Mantén los dedos claramente separados

Para un mejor reconocimiento de expresiones faciales:
- Asegura que el rostro esté bien iluminado y claramente visible
- Posiciona el rostro en el centro del marco
- Haz expresiones más pronunciadas para una mejor detección

## 📚 Referencias

- [Documentación de MediaPipe](https://google.github.io/mediapipe/)
- [Documentación de OpenCV](https://docs.opencv.org/)
- [Técnicas de Visión por Computadora](https://opencv.org/)

