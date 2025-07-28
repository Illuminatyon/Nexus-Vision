# Reconnaissance Vidéo Python v1

[English](#english) | [Français](#français)

---

<a name="english"></a>
# Video Recognition Python v1

This program uses your webcam to detect hands and count extended fingers, as well as recognize facial expressions. It can detect both hands simultaneously, calculate the total sum of extended fingers, and identify different facial expressions.

## Requirements

- Python 3.6 or higher
- Webcam
- The following Python libraries:
  - opencv-python
  - mediapipe
  - numpy

## Installation

1. Clone or download this repository

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

   Or install individually:
   ```
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   ```

## Usage

1. Run the program:
   ```
   python main.py
   ```

2. Show your hands to the camera:
   - RIGHT HAND: Show any number of fingers (0-5)
   - LEFT HAND: Show any number of fingers (0-5)
   - The program will count and display the number of extended fingers on each hand
   - The program will also calculate and display the total sum of all extended fingers on both hands

3. Facial expression recognition:
   - Position your face in front of the camera
   - The program will detect and display your facial expression
   - Supported expressions:
     * Smile: Detected when you smile (mouth width increases)
     * Surprise: Detected when you raise your eyebrows and open your mouth
     * Neutral: Default expression when no specific expression is detected
   - The program shows the detected expression and a confidence percentage

4. Press 'q' to quit the program

## Troubleshooting

### Check Libraries

Run the library check script to verify if all required libraries are installed correctly:

```
python check_libraries.py
```

This script will:
- Check if all required libraries are installed
- Verify if the installed versions meet the minimum requirements
- Provide troubleshooting tips for any issues found

### Common Issues

#### Library Issues

If you encounter issues with libraries:

1. Make sure you have installed all required dependencies
2. Check that your Python version is compatible (3.6+)
3. If using Windows, you might need to install Visual C++ build tools:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - During installation, select "Desktop development with C++"

4. For MediaPipe installation issues:
   - Try: `pip install --upgrade mediapipe`
   - Or specify version: `pip install mediapipe==0.8.9`

5. For OpenCV camera access issues:
   - Make sure your webcam is properly connected
   - Try a different USB port
   - Check if other applications are using the camera

#### Hand Detection Issues

If you have problems with hand detection:

1. **Left Hand Detection Issues**:
   - Make sure your palm is facing the camera
   - Position your left hand so the thumb is on the left side
   - Try rotating your hand slightly if it's being misidentified
   - Keep your fingers clearly separated when extending them
   - For thumb detection:
     * Extend your thumb clearly to the side (away from your palm)
     * For accurate detection, make sure your thumb is fully extended and clearly separated from your palm
     * Orange circles on thumb landmarks indicate when the thumb is not extended
     * A green circle appears when the thumb is successfully detected

2. **Right Hand Detection Issues**:
   - Make sure your palm is facing the camera
   - Position your right hand so the thumb is on the right side
   - Try rotating your hand slightly if it's being misidentified
   - Keep your fingers clearly separated when extending them
   - For thumb detection:
     * Extend your thumb clearly to the side (away from your palm)
     * For accurate detection, make sure your thumb is fully extended and clearly separated from your palm
     * Orange circles on thumb landmarks indicate when the thumb is not extended
     * A magenta circle appears when the thumb is successfully detected

3. **Facial Expression Recognition Issues**:
   - Make sure your face is well-lit and clearly visible
   - Position your face in the center of the frame
   - For best results:
     * Smile: Make a clear, natural smile
     * Surprise: Raise your eyebrows and open your mouth
     * Neutral: Relax your facial muscles
   - If expressions are not being detected correctly:
     * Try adjusting your position or the lighting
     * Make more pronounced expressions
     * Ensure your face is fully visible and not partially out of frame

4. **General Tips**:
   - Ensure good lighting conditions
   - Avoid busy backgrounds
   - Keep your hand within the camera frame
   - Look at the debug information on screen for guidance
   - Yellow circles indicate which fingers are being detected as extended

---

<a name="français"></a>
# Reconnaissance Vidéo Python v1

Ce programme utilise votre webcam pour détecter les mains et compter les doigts tendus, ainsi que pour reconnaître les expressions faciales. Il peut détecter les deux mains simultanément, calculer la somme totale des doigts tendus et identifier différentes expressions faciales.

## Prérequis

- Python 3.6 ou supérieur
- Webcam
- Les bibliothèques Python suivantes :
  - opencv-python
  - mediapipe
  - numpy

## Installation

1. Clonez ou téléchargez ce dépôt

2. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

   Ou installez-les individuellement :
   ```
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   ```

## Utilisation

1. Exécutez le programme :
   ```
   python main.py
   ```

2. Montrez vos mains à la caméra :
   - MAIN DROITE : Montrez n'importe quel nombre de doigts (0-5)
   - MAIN GAUCHE : Montrez n'importe quel nombre de doigts (0-5)
   - Le programme comptera et affichera le nombre de doigts tendus sur chaque main
   - Le programme calculera et affichera également la somme totale de tous les doigts tendus sur les deux mains

3. Reconnaissance des expressions faciales :
   - Positionnez votre visage devant la caméra
   - Le programme détectera et affichera votre expression faciale
   - Expressions prises en charge :
     * Sourire : Détecté lorsque vous souriez (la largeur de la bouche augmente)
     * Surprise : Détectée lorsque vous levez les sourcils et ouvrez la bouche
     * Neutre : Expression par défaut lorsqu'aucune expression spécifique n'est détectée
   - Le programme affiche l'expression détectée et un pourcentage de confiance

4. Appuyez sur 'q' pour quitter le programme

## Dépannage

### Vérification des bibliothèques

Exécutez le script de vérification des bibliothèques pour vérifier si toutes les bibliothèques requises sont correctement installées :

```
python check_libraries.py
```

Ce script va :
- Vérifier si toutes les bibliothèques requises sont installées
- Vérifier si les versions installées répondent aux exigences minimales
- Fournir des conseils de dépannage pour tout problème trouvé

### Problèmes courants

#### Problèmes de bibliothèques

Si vous rencontrez des problèmes avec les bibliothèques :

1. Assurez-vous d'avoir installé toutes les dépendances requises
2. Vérifiez que votre version de Python est compatible (3.6+)
3. Si vous utilisez Windows, vous pourriez avoir besoin d'installer les outils de build Visual C++ :
   - Téléchargez-les depuis : https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Pendant l'installation, sélectionnez "Développement Desktop avec C++"

4. Pour les problèmes d'installation de MediaPipe :
   - Essayez : `pip install --upgrade mediapipe`
   - Ou spécifiez la version : `pip install mediapipe==0.8.9`

5. Pour les problèmes d'accès à la caméra avec OpenCV :
   - Assurez-vous que votre webcam est correctement connectée
   - Essayez un port USB différent
   - Vérifiez si d'autres applications utilisent la caméra

#### Problèmes de détection des mains

Si vous avez des problèmes avec la détection des mains :

1. **Problèmes de détection de la main gauche** :
   - Assurez-vous que votre paume est face à la caméra
   - Positionnez votre main gauche de sorte que le pouce soit sur le côté gauche
   - Essayez de tourner légèrement votre main si elle est mal identifiée
   - Gardez vos doigts clairement séparés lorsque vous les tendez
   - Pour la détection du pouce :
     * Étendez clairement votre pouce sur le côté (loin de votre paume)
     * Pour une détection précise, assurez-vous que votre pouce est complètement tendu et clairement séparé de votre paume
     * Des cercles orange sur les repères du pouce indiquent quand le pouce n'est pas tendu
     * Un cercle vert apparaît lorsque le pouce est détecté avec succès

2. **Problèmes de détection de la main droite** :
   - Assurez-vous que votre paume est face à la caméra
   - Positionnez votre main droite de sorte que le pouce soit sur le côté droit
   - Essayez de tourner légèrement votre main si elle est mal identifiée
   - Gardez vos doigts clairement séparés lorsque vous les tendez
   - Pour la détection du pouce :
     * Étendez clairement votre pouce sur le côté (loin de votre paume)
     * Pour une détection précise, assurez-vous que votre pouce est complètement tendu et clairement séparé de votre paume
     * Des cercles orange sur les repères du pouce indiquent quand le pouce n'est pas tendu
     * Un cercle magenta apparaît lorsque le pouce est détecté avec succès

3. **Problèmes de reconnaissance des expressions faciales** :
   - Assurez-vous que votre visage est bien éclairé et clairement visible
   - Positionnez votre visage au centre du cadre
   - Pour de meilleurs résultats :
     * Sourire : Faites un sourire clair et naturel
     * Surprise : Levez vos sourcils et ouvrez votre bouche
     * Neutre : Détendez vos muscles faciaux
   - Si les expressions ne sont pas correctement détectées :
     * Essayez d'ajuster votre position ou l'éclairage
     * Faites des expressions plus prononcées
     * Assurez-vous que votre visage est entièrement visible et pas partiellement hors cadre

4. **Conseils généraux** :
   - Assurez-vous d'avoir de bonnes conditions d'éclairage
   - Évitez les arrière-plans chargés
   - Gardez votre main dans le cadre de la caméra
   - Consultez les informations de débogage à l'écran pour vous guider
   - Les cercles jaunes indiquent quels doigts sont détectés comme tendus
