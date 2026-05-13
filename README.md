# iPiano — Application d'Apprentissage du Piano par Vision par Ordinateur

**iPiano** est une application Python interactive qui utilise votre webcam pour détecter vos mains en temps réel et vous permettre de jouer sur un piano virtuel superposé à l'image. Elle propose un mode exercice guidé, un système de score avec combo, un **feedback intelligent par IA**, et une interface inspirée du design iOS (Glassmorphism).

---

## Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| **Tracking des mains** | Détection jusqu'à 2 mains via MediaPipe HandLandmarker (précision haute) |
| **Piano virtuel** | 7 à 14 touches blanches + touches noires superposées à la vidéo |
| **Mode exercice** | Note cible affichée à l'écran, validation automatique |
| **Système de score** | Score progressif avec bonus combo (×2, ×3…) |
| **Feedback IA** | Conseils en temps réel par **SambaNova (DeepSeek-V3.1)** pour améliorer votre jeu |
| **Son de piano** | Lecture des notes jouées via Pygame |
| **Design iOS** | Interface Glassmorphism, coins arrondis, barre de progression |
| **Paramètres** | Calibration de la hauteur, taille des touches et sensibilité via sliders, avec **bouton de réinitialisation** |
| **Thread séparé** | Traitement vidéo en thread dédié pour garantir la fluidité de l'UI |

---

## Architecture du Code (POO)

```
ipiano.py
├── class HandTracker       — Détection MediaPipe HandLandmarker (Tasks API ≥ 0.10)
│   ├── process_frame()     — Traite une frame et dessine les landmarks
│   └── get_finger_tips()   — Retourne les coordonnées pixel des extrémités de doigts
│
├── class VirtualPiano      — Piano virtuel, logique de jeu et score
│   ├── update_layout()     — Recalcule la géométrie selon la largeur de la frame
│   ├── check_press()       — Détecte les touches pressées et met à jour le score (joue le son)
│   ├── set_new_target()    — Choisit une nouvelle note cible aléatoire
│   └── draw()              — Dessine le piano sur la frame (effet glassmorphism)
│
├── class SoundPlayer       — Gestion de la lecture des sons de piano (Pygame)
│   ├── _load_sounds()      — Charge les fichiers .wav des notes
│   └── play_note()         — Joue une note spécifique
│
├── class AIFeedback        — Intégration de l'IA pour le feedback (SambaNova/Mistral)
│   └── get_feedback()      — Génère un conseil basé sur la performance actuelle
│
└── class PianoApp          — Interface CustomTkinter (hérite de CTk)
    ├── _build_landing()    — Page d'accueil avec logo et boutons
    ├── _build_lesson()     — Page de leçon (vidéo + barre de progression + feedback IA)
    ├── _build_settings()   — Page de paramètres avec sliders iOS et bouton de réinitialisation
    ├── _start_lesson()     — Ouvre la webcam et démarre le thread vidéo
    ├── _video_loop()       — Boucle de capture/traitement (thread séparé)
    └── _update_ui()        — Mise à jour thread-safe de l'interface
```

---

## Guide d'Installation pour VSCode

### Prérequis

- **Python 3.9 ou supérieur** ([python.org](https://www.python.org/downloads/))
- **Visual Studio Code** ([code.visualstudio.com](https://code.visualstudio.com/))
- **Extension Python** pour VSCode (identifiant : `ms-python.python`)
- **Webcam** fonctionnelle connectée à votre ordinateur

### Étape 1 — Ouvrir le projet dans VSCode

Ouvrez VSCode, puis via `Fichier > Ouvrir le dossier`, sélectionnez le dossier contenant `ipiano.py`, `requirements.txt` et `README.md`.

### Étape 2 — Créer un environnement virtuel

Ouvrez un terminal intégré dans VSCode (`Terminal > Nouveau terminal`) et exécutez :

```bash
# macOS / Linux
python3 -m venv venv

# Windows
python -m venv venv
```

### Étape 3 — Activer l'environnement virtuel

```bash
# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat
```

> **Note VSCode :** Après activation, sélectionnez l'interpréteur `venv` via `Ctrl+Shift+P > Python: Select Interpreter` et choisissez `./venv/bin/python`.

### Étape 4 — Installer les dépendances

```bash
pip install -r requirements.txt
```

L'installation prend environ 2 à 5 minutes selon votre connexion (MediaPipe, OpenCV, Pygame, OpenAI sont volumineux).

### Étape 5 — Télécharger le modèle MediaPipe

iPiano utilise la **Tasks API de MediaPipe (≥ 0.10)** qui nécessite un fichier modèle externe. Téléchargez-le et placez-le dans le **même dossier** que `ipiano.py` :

```bash
# macOS / Linux
curl -O "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "hand_landmarker.task"
```

Le fichier fait environ **7,5 Mo**.

### Étape 6 — Générer les sons de piano

L'application nécessite des fichiers `.wav` pour chaque note. Exécutez le script suivant une fois dans votre terminal VSCode. Il créera un dossier `sounds/` et y placera les fichiers nécessaires :

```bash
python -c "\
import numpy as np, wave, os\
\
def generate_piano_note(freq, filename, duration=1.0, sample_rate=44100):\
    t = np.linspace(0, duration, int(sample_rate * duration), False)\
    audio = np.sin(2 * np.pi * freq * t) * np.exp(-3 * t)\
    audio += 0.5 * np.sin(2 * np.pi * (2 * freq) * t) * np.exp(-5 * t)\
    audio += 0.25 * np.sin(2 * np.pi * (3 * freq) * t) * np.exp(-7 * t)\
    audio = (audio * 32767 / np.max(np.abs(audio))).astype(np.int16)\
    with wave.open(filename, 'w') as f:\
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sample_rate); f.writeframes(audio.tobytes())\
\
os.makedirs('sounds', exist_ok=True)\
notes = {\"C\": 261.63, \"C#\": 277.18, \"D\": 293.66, \"D#\": 311.13, \"E\": 329.63, \"F\": 349.23, \"F#\": 369.99, \"G\": 392.00, \"G#\": 415.30, \"A\": 440.00, \"A#\": 466.16, \"B\": 493.88}\
\
for name, freq in notes.items():\
    generate_piano_note(freq, f\"sounds/{name.replace('#', 's')}.wav\")\
    print(f\"Generated {name}\")\
"
```

### Étape 7 — Lancer l'application

```bash
python ipiano.py
```

Ou directement depuis VSCode via le bouton **▶ Run Python File** en haut à droite.

---

## Structure des fichiers

```
LearnPiano/
├── ipiano.py               ← Application principale
├── requirements.txt        ← Dépendances Python
├── README.md               ← Ce guide
├── hand_landmarker.task    ← Modèle MediaPipe (à télécharger)
└── sounds/                 ← Dossier contenant les fichiers .wav des notes (à générer)
    ├── C.wav
    ├── Cs.wav
    ├── D.wav
    └── ...
```

---

## Utilisation

### Page d'accueil
Au lancement, la **Landing Page** s'affiche avec le logo iPiano. Cliquez sur **"Commencer la leçon"** pour démarrer ou **"Paramètres"** pour configurer le piano.

### Mode Leçon
La webcam s'active et affiche votre image en miroir. Le **piano virtuel** apparaît en bas de l'écran. La note à jouer est indiquée en haut en gras. Placez l'extrémité de votre doigt (index ou autre) sur la touche correspondante pour valider. Un son de piano sera joué à chaque pression de touche.

Les touches s'illuminent en **bleu** lorsqu'elles sont pressées. La touche cible est entourée d'un **cadre rouge**. Le score augmente à chaque bonne note, avec un **bonus combo** si vous enchaînez plusieurs notes correctes rapidement. Un **professeur IA** vous donnera des conseils en temps réel pour vous aider à progresser.

### Paramètres de calibration

| Paramètre | Description | Plage |
|---|---|---|
| Hauteur du piano | Position verticale du piano dans l'image | 100 – 580 px |
| Largeur des touches | Largeur de chaque touche blanche | 40 – 140 px |
| Hauteur des touches | Hauteur des touches blanches | 60 – 180 px |
| Sensibilité | Fraction de la touche à atteindre pour déclencher | 0.40 – 1.0 |
| Nombre de touches | Nombre de touches blanches affichées | 5 – 14 |

Un bouton **"Réinitialiser les paramètres"** est disponible pour restaurer toutes les valeurs par défaut.

---

## Dépannage

**La webcam ne s'ouvre pas** : Vérifiez que votre webcam est bien connectée et qu'aucune autre application ne l'utilise. Sur macOS, accordez les permissions caméra à Terminal/VSCode dans `Préférences Système > Confidentialité > Caméra`.

**Modèle introuvable** : Assurez-vous que `hand_landmarker.task` est dans le même dossier que `ipiano.py`. L'application affiche un avertissement sur la page d'accueil si le fichier est absent.

**Sons non joués** : Assurez-vous que le dossier `sounds/` existe et contient les fichiers `.wav` générés à l'étape 6. Vérifiez également que Pygame est correctement installé et que le volume de votre système est activé.

**Performances lentes** : Réduisez la résolution de la webcam ou fermez les autres applications. Le traitement MediaPipe est optimisé pour CPU mais bénéficie d'un GPU si disponible.

**Erreur `ModuleNotFoundError`** : Vérifiez que l'environnement virtuel est bien activé (`(venv)` doit apparaître dans votre terminal) et que `pip install -r requirements.txt` a été exécuté avec succès.

---

## Dépendances

| Bibliothèque | Version minimale | Rôle |
|---|---|---|
| `mediapipe` | 0.10.0 | Détection des mains (HandLandmarker) |
| `opencv-python` | 4.8.0 | Capture vidéo et traitement d'image |
| `customtkinter` | 5.2.0 | Interface graphique iOS-like |
| `Pillow` | 10.0.0 | Conversion d'images pour Tkinter |
| `numpy` | 1.24.0 | Manipulation des arrays d'images |
| `pygame` | 2.0.0 | Lecture des sons de piano |
| `openai` | 1.0.0 | Accès aux API LLM (SambaNova, Mistral) |



# TO RUN : 
## 1. Créer et activer l'environnement virtuel
```bash
python3 -m venv venv && source venv/bin/activate
```
## 2. Installer les dépendances
```bash
pip install -r requirements.txt
```
## 3. Télécharger le modèle MediaPipe (7,5 Mo — OBLIGATOIRE)
```bash
curl -O "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
```
## 4. Lancer iPiano
```bash
python ipiano.py
```
