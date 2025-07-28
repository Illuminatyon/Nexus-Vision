# Video Recognition Python

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![University: Paris 8](https://img.shields.io/badge/University-Paris%208-blue)
![Computer: Vision](https://img.shields.io/badge/Computer-Vision-orange)
![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-red)
![Contributors](https://img.shields.io/badge/Contributors-1-brightgreen)
![Stars](https://img.shields.io/badge/Stars-0-lightgrey)
![Fork](https://img.shields.io/badge/Forks-0-lightgrey)
![Watchers](https://img.shields.io/badge/Watchers-0-lightgrey)

## 🌍 Multilingual README Versions

| 🇫🇷 [Français](README.fr.md) | 🇬🇧 English (you are here) | 🇪🇸 [Español](README.es.md) |
|------------------------------|----------------------------|----------------------------|
| [Switch to French](README.fr.md) | Current language | [Switch to Spanish](README.es.md) |

## 📘 Project Overview

This project is a computer vision application that uses your webcam to detect hands and recognize facial expressions. The main features include:

- Real-time hand detection and finger counting
- Facial expression recognition (smile, surprise, neutral)
- Support for both hands simultaneously
- Calculation of the total sum of extended fingers
- Visual feedback with confidence scores

The application was developed to explore the capabilities of computer vision libraries and to create an interactive demonstration of gesture and expression recognition.

## 📊 Features

### Hand Detection and Finger Counting
- Detects both left and right hands
- Counts extended fingers (0-5) on each hand
- Calculates the total sum of extended fingers
- Provides visual feedback for detected fingers

### Facial Expression Recognition
- Detects three expressions:
  - Smile: When mouth corners are raised
  - Surprise: When eyebrows are raised and mouth is open
  - Neutral: Default expression
- Shows confidence percentage for detected expressions
- Displays the expression above the user's head

## ⚙️ How It Works

The application uses two main computer vision technologies:

1. **MediaPipe Hands**
   - Detects hand landmarks (21 points per hand)
   - Tracks finger positions and movements
   - Determines if fingers are extended or folded

2. **MediaPipe Face Mesh**
   - Detects facial landmarks (468 points)
   - Tracks key facial features (eyes, eyebrows, mouth)
   - Analyzes landmark positions to determine expressions

The application processes each video frame to:
1. Detect hands and face
2. Analyze landmark positions
3. Count extended fingers
4. Recognize facial expressions
5. Display results with visual feedback

## 🧑‍💻 Technologies Used

- **Python**: Core programming language
- **OpenCV**: Computer vision and image processing
- **MediaPipe**: Hand and face detection frameworks
- **NumPy**: Numerical computations

## 💻 Installation

### Prerequisites
- Python 3.6 or higher
- Webcam
- Windows, macOS, or Linux

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Illuminatyon/Nexus-Vision
   cd Nexus-Vision
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   ```

3. Verify installation:
   ```bash
   python check_libraries.py
   ```

## 📝 Usage

### Running the Application

```bash
python main.py
```

For debug mode (shows additional visualization):
```bash
python main.py --debug
```

### Controls and Interaction

1. **Hand Gestures**:
   - Show your hands to the camera
   - Extend or fold fingers to change the count
   - Both hands can be detected simultaneously

2. **Facial Expressions**:
   - Position your face in front of the camera
   - Smile to trigger smile detection
   - Raise eyebrows and open mouth for surprise detection
   - Relax facial muscles for neutral expression

3. **Exit**:
   - Press 'q' to quit the application

## 🔍 Troubleshooting

### Library Issues

If you encounter problems with libraries:

1. Run the check script:
   ```bash
   python check_libraries.py
   ```

2. For MediaPipe issues:
   ```bash
   pip install --upgrade mediapipe
   ```

3. For OpenCV camera access:
   - Ensure your webcam is properly connected
   - Check if other applications are using the camera

### Detection Issues

For better hand detection:
- Ensure good lighting conditions
- Keep hands within camera frame
- Position palms facing the camera
- Keep fingers clearly separated

For better facial expression recognition:
- Ensure face is well-lit and clearly visible
- Position face in center of frame
- Make more pronounced expressions for better detection

## 📚 References

- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Computer Vision Techniques](https://opencv.org/)

