# Reconnaissance Vidéo Python

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![University: Paris 8](https://img.shields.io/badge/University-Paris%208-blue)
![Computer: Vision](https://img.shields.io/badge/Computer-Vision-orange)
![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-red)
![Contributors](https://img.shields.io/badge/Contributors-1-brightgreen)
![Stars](https://img.shields.io/badge/Stars-0-lightgrey)
![Fork](https://img.shields.io/badge/Forks-0-lightgrey)
![Watchers](https://img.shields.io/badge/Watchers-0-lightgrey)

## 🌍 Versions Multilingues du README

| 🇫🇷 Français (vous êtes ici) | 🇬🇧 [English](README.md) | 🇪🇸 [Español](README.es.md) |
|------------------------------|----------------------------|----------------------------|
| Langue actuelle | [Passer à l'anglais](README.md) | [Passer à l'espagnol](README.es.md) |

## 📘 Aperçu du Projet

Ce projet est une application de vision par ordinateur qui utilise votre webcam pour détecter les mains et reconnaître les expressions faciales. Les principales fonctionnalités comprennent :

- Détection des mains et comptage des doigts en temps réel
- Reconnaissance des expressions faciales (sourire, surprise, neutre)
- Prise en charge simultanée des deux mains
- Calcul de la somme totale des doigts étendus
- Retour visuel avec scores de confiance

L'application a été développée pour explorer les capacités des bibliothèques de vision par ordinateur et pour créer une démonstration interactive de reconnaissance de gestes et d'expressions.

## 📊 Fonctionnalités

### Détection des Mains et Comptage des Doigts
- Détecte les mains gauche et droite
- Compte les doigts étendus (0-5) sur chaque main
- Calcule la somme totale des doigts étendus
- Fournit un retour visuel pour les doigts détectés

### Reconnaissance des Expressions Faciales
- Détecte trois expressions :
  - Sourire : Lorsque les coins de la bouche sont relevés
  - Surprise : Lorsque les sourcils sont levés et la bouche est ouverte
  - Neutre : Expression par défaut
- Affiche le pourcentage de confiance pour les expressions détectées
- Affiche l'expression au-dessus de la tête de l'utilisateur

## ⚙️ Comment Ça Fonctionne

L'application utilise deux principales technologies de vision par ordinateur :

1. **MediaPipe Hands**
   - Détecte les points de repère des mains (21 points par main)
   - Suit les positions et mouvements des doigts
   - Détermine si les doigts sont étendus ou pliés

2. **MediaPipe Face Mesh**
   - Détecte les points de repère du visage (468 points)
   - Suit les caractéristiques faciales clés (yeux, sourcils, bouche)
   - Analyse les positions des points de repère pour déterminer les expressions

L'application traite chaque image vidéo pour :
1. Détecter les mains et le visage
2. Analyser les positions des points de repère
3. Compter les doigts étendus
4. Reconnaître les expressions faciales
5. Afficher les résultats avec un retour visuel

## 🧑‍💻 Technologies Utilisées

- **Python** : Langage de programmation principal
- **OpenCV** : Vision par ordinateur et traitement d'images
- **MediaPipe** : Frameworks de détection des mains et du visage
- **NumPy** : Calculs numériques

## 💻 Installation

### Prérequis
- Python 3.6 ou supérieur
- Webcam
- Windows, macOS ou Linux

### Configuration

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Illuminatyon/video-recognition-python.git
   cd video-recognition-python
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

   Ou installer individuellement :
   ```bash
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   ```

3. Vérifier l'installation :
   ```bash
   python check_libraries.py
   ```

## 📝 Utilisation

### Exécution de l'Application

```bash
python main.py
```

Pour le mode debug (affiche des visualisations supplémentaires) :
```bash
python main.py --debug
```

### Contrôles et Interaction

1. **Gestes de la Main** :
   - Montrez vos mains à la caméra
   - Étendez ou pliez les doigts pour changer le comptage
   - Les deux mains peuvent être détectées simultanément

2. **Expressions Faciales** :
   - Positionnez votre visage devant la caméra
   - Souriez pour déclencher la détection du sourire
   - Levez les sourcils et ouvrez la bouche pour la détection de surprise
   - Détendez les muscles du visage pour l'expression neutre

3. **Quitter** :
   - Appuyez sur 'q' pour quitter l'application

## 🔍 Dépannage

### Problèmes de Bibliothèques

Si vous rencontrez des problèmes avec les bibliothèques :

1. Exécutez le script de vérification :
   ```bash
   python check_libraries.py
   ```

2. Pour les problèmes de MediaPipe :
   ```bash
   pip install --upgrade mediapipe
   ```

3. Pour l'accès à la caméra OpenCV :
   - Assurez-vous que votre webcam est correctement connectée
   - Vérifiez si d'autres applications utilisent la caméra

### Problèmes de Détection

Pour une meilleure détection des mains :
- Assurez-vous de bonnes conditions d'éclairage
- Gardez les mains dans le cadre de la caméra
- Positionnez les paumes face à la caméra
- Gardez les doigts clairement séparés

Pour une meilleure reconnaissance des expressions faciales :
- Assurez-vous que le visage est bien éclairé et clairement visible
- Positionnez le visage au centre du cadre
- Faites des expressions plus prononcées pour une meilleure détection

## 📚 Références

- [Documentation MediaPipe](https://google.github.io/mediapipe/)
- [Documentation OpenCV](https://docs.opencv.org/)
- [Techniques de Vision par Ordinateur](https://opencv.org/)

