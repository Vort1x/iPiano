import cv2
import mediapipe as mp
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision import (
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarkerResult,
    RunningMode,
)

import os
import threading
import time
import random
import sys
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  TRADUCTIONS
# ─────────────────────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "FR": {
        "title": "iPiano",
        "subtitle": "Apprenez le piano avec vos mains",
        "start_lesson": "Commencer la leçon",
        "free_play": "Mode Libre",
        "settings": "Paramètres",
        "back": "Retour",
        "score": "Score",
        "progression": "Progression",
        "play_note": "JOUE LA NOTE :",
        "finished": "Mélodie Terminée ! 🎉",
        "choose_melody": "Choisissez une mélodie :",
        "reset": "Réinitialiser",
        "language": "Langue",
        "height": "Hauteur du piano",
        "width": "Largeur des touches",
        "key_height": "Hauteur des touches",
        "sensitivity": "Sensibilité",
        "num_keys": "Nombre de touches",
        "camera_source": "Source Caméra",
        "desk_view": "Mode Desk View (Mac)",
        "rotate_piano": "Rotation 180°",
        "paper_mode": "Mode Papier (Bêta)",
        "download_template": "Télécharger le Gabarit Piano A4",
        "free_play_title": "Mode Libre - Amusez-vous !",
        "model_missing": "⚠ Modèle MediaPipe manquant",
        "segmenter_missing": "⚠ Modèle de segmentation manquant (mains non isolées).",
    },
    "EN": {
        "title": "iPiano",
        "subtitle": "Learn piano with your hands",
        "start_lesson": "Start Lesson",
        "free_play": "Free Play",
        "settings": "Settings",
        "back": "Back",
        "score": "Score",
        "progression": "Progress",
        "play_note": "PLAY THE NOTE:",
        "finished": "Melody Finished! 🎉",
        "choose_melody": "Choose a melody:",
        "reset": "Reset",
        "language": "Language",
        "height": "Piano Height",
        "width": "Key Width",
        "key_height": "Key Height",
        "sensitivity": "Sensitivity",
        "num_keys": "Number of Keys",
        "paper_mode": "Paper Mode (Beta)",
        "download_template": "Download A4 Piano Template",
        "free_play_title": "Free Play - Have fun!",
        "model_missing": "⚠ MediaPipe Model Missing",
        "segmenter_missing": "⚠ Segmentation Model Missing",
    },
    "IT": {
        "title": "iPiano",
        "subtitle": "Impara il piano con le tue mani",
        "start_lesson": "Inizia Lezione",
        "free_play": "Modalità Libera",
        "settings": "Impostazioni",
        "back": "Indietro",
        "score": "Punteggio",
        "progression": "Progressione",
        "play_note": "SUONA LA NOTA:",
        "finished": "Melodia Finita! 🎉",
        "choose_melody": "Scegli una melodia:",
        "reset": "Ripristina",
        "language": "Lingua",
        "height": "Altezza Piano",
        "width": "Larghezza Tasti",
        "key_height": "Altezza Tasti",
        "sensitivity": "Sensibilità",
        "num_keys": "Numero di Tasti",
        "free_play_title": "Modalità Libera - Divertiti!",
        "model_missing": "⚠ Modello MediaPipe mancante",
        "segmenter_missing": "⚠ Modello di segmentazione mancante",
    },
    "ES": {
        "title": "iPiano",
        "subtitle": "Aprende piano con tus manos",
        "start_lesson": "Empezar Lección",
        "free_play": "Modo Libre",
        "settings": "Ajustes",
        "back": "Volver",
        "score": "Puntuación",
        "progression": "Progresión",
        "play_note": "TOCA LA NOTA:",
        "finished": "¡Melodía Terminada! 🎉",
        "choose_melody": "Elige una melodía:",
        "reset": "Restablecer",
        "language": "Idioma",
        "height": "Altura del Piano",
        "width": "Anchura de Teclas",
        "key_height": "Altura de Teclas",
        "sensitivity": "Sensibilidad",
        "num_keys": "Número de Teclas",
        "free_play_title": "Modo Libre - ¡Diviértete!",
        "model_missing": "⚠ Modelo MediaPipe ausente",
        "segmenter_missing": "⚠ Modelo de segmentación ausente",
    },
    "PT": {
        "title": "iPiano",
        "subtitle": "Aprenda piano com suas mãos",
        "start_lesson": "Começar Lição",
        "free_play": "Modo Livre",
        "settings": "Configurações",
        "back": "Voltar",
        "score": "Pontuação",
        "progression": "Progressão",
        "play_note": "TOQUE A NOTA:",
        "finished": "Melodia Terminada! 🎉",
        "choose_melody": "Escolha uma melodia:",
        "reset": "Redefinir",
        "language": "Idioma",
        "height": "Altura do Piano",
        "width": "Largura das Teclas",
        "key_height": "Altura das Teclas",
        "sensitivity": "Sensibilidade",
        "num_keys": "Número de Teclas",
        "free_play_title": "Modo Livre - Divirta-se!",
        "model_missing": "⚠ Modelo MediaPipe ausente",
        "segmenter_missing": "⚠ Modelo de segmentación ausente",
    }
}

# ─────────────────────────────────────────────────────────────────────────────
#  MÉLODIES ALLONGÉES
# ─────────────────────────────────────────────────────────────────────────────
MELODIES = {
    "Au Clair de la Lune": ["C", "C", "C", "D", "E", "D", "C", "E", "D", "D", "C", "C", "C", "C", "D", "E", "D", "C", "E", "D", "D", "C"],
    "Frère Jacques": ["C", "D", "E", "C", "C", "D", "E", "C", "E", "F", "G", "E", "F", "G", "G", "A", "G", "F", "E", "C", "G", "A", "G", "F", "E", "C", "C", "G", "C", "C", "G", "C"],
    "Vive le Vent": ["E", "E", "E", "E", "E", "E", "E", "G", "C", "D", "E", "F", "F", "F", "F", "F", "E", "E", "E", "E", "D", "D", "E", "D", "G"],
    "Ode à la Joie": ["E", "E", "F", "G", "G", "F", "E", "D", "C", "C", "D", "E", "E", "D", "C", "C", "D", "E", "E", "F", "G", "G", "F", "E", "D", "C", "C", "D", "E", "D", "C", "C"],
}

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTES GLOBALES
# ─────────────────────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(_SCRIPT_DIR, "hand_landmarker.task")
SOUNDS_DIR  = os.path.join(_SCRIPT_DIR, "sounds")

HAND_CONNECTIONS: list[tuple[int, int]] = [
    (0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17),
]


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE : SoundPlayer
# ─────────────────────────────────────────────────────────────────────────────
class SoundPlayer:
    def __init__(self, sounds_dir: str = SOUNDS_DIR) -> None:
        pygame.mixer.init()
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._load_sounds(sounds_dir)

    def _load_sounds(self, sounds_dir: str) -> None:
        if not os.path.exists(sounds_dir): return
        for filename in os.listdir(sounds_dir):
            if filename.endswith(".wav"):
                # Gérer les noms comme C4.wav ou Cs4.wav (C#4)
                note_id = filename.replace(".wav", "").replace("s", "#")
                try: self._sounds[note_id] = pygame.mixer.Sound(os.path.join(sounds_dir, filename))
                except: pass

    def play_note(self, note_name: str, octave: int = 4) -> None:
        # Essayer de jouer la note avec octave (ex: C4)
        note_id = f"{note_name}{octave}"
        sound = self._sounds.get(note_id)
        
        # Fallback sur la note sans octave si non trouvée
        if not sound:
            sound = self._sounds.get(note_name)
            
        if sound: sound.play()

    def close(self) -> None: pygame.mixer.quit()


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE : HandTracker
# ─────────────────────────────────────────────────────────────────────────────
class HandTracker:
    FINGER_TIPS: list[int] = [4, 8, 12, 16, 20]

    def __init__(self, model_path: str = MODEL_PATH) -> None:
        if not os.path.exists(model_path): raise FileNotFoundError("hand_landmarker.task")

        options = HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.VIDEO, num_hands=2,
            min_hand_detection_confidence=0.75, min_hand_presence_confidence=0.75, min_tracking_confidence=0.75,
        )
        self._detector = HandLandmarker.create_from_options(options)
        self._last_result: HandLandmarkerResult | None = None
        self._frame_ts: int = 0

    def process_frame(self, frame: np.ndarray, draw: bool = True) -> np.ndarray:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self._frame_ts += 33

        self._last_result = self._detector.detect_for_video(mp_image, self._frame_ts)
        
        hand_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        if self._last_result and self._last_result.hand_landmarks:
            h, w = frame.shape[:2]
            for hand_lms in self._last_result.hand_landmarks:
                points = np.array([[[int(lm.x * w), int(lm.y * h)]] for lm in hand_lms], dtype=np.int32)
                hull = cv2.convexHull(points)
                cv2.fillPoly(hand_mask, [hull], 255)

        if draw: self.draw_landmarks(frame)
        
        return hand_mask

    def draw_landmarks(self, frame: np.ndarray) -> None:
        if not self._last_result or not self._last_result.hand_landmarks: return
        h, w = frame.shape[:2]
        for hand_lms in self._last_result.hand_landmarks:
            pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_lms]
            for a, b in HAND_CONNECTIONS: cv2.line(frame, pts[a], pts[b], (100, 180, 255), 2, cv2.LINE_AA)
            for i, (px, py) in enumerate(pts):
                color = (255, 255, 255) if i not in self.FINGER_TIPS else (0, 200, 255)
                cv2.circle(frame, (px, py), 5, color, cv2.FILLED)
                cv2.circle(frame, (px, py), 5, (80, 80, 80), 1)

    def get_finger_tips(self, frame: np.ndarray) -> list[tuple[int, int, int, float]]:
        tips = []
        if not self._last_result or not self._last_result.hand_landmarks: return tips
        h, w = frame.shape[:2]
        for hand_lms in self._last_result.hand_landmarks:
            for tip_id in self.FINGER_TIPS:
                lm = hand_lms[tip_id]
                # x, y sont normalisés (0-1), z représente la profondeur par rapport au poignet
                tips.append((tip_id, int(lm.x * w), int(lm.y * h), lm.z))
        return tips

    def close(self) -> None:
        self._detector.close()


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE : VirtualPiano
# ─────────────────────────────────────────────────────────────────────────────
class VirtualPiano:
    def __init__(self, app_instance: ctk.CTk, num_keys: int = 14, piano_height_ratio: float = 0.3, key_width_ratio: float = 0.07, key_height_ratio: float = 0.6, sensitivity: float = 0.6, **kwargs) -> None:
        self.app = app_instance
        self.num_keys = num_keys
        self.piano_height_ratio = piano_height_ratio
        self.key_width_ratio = key_width_ratio
        self.key_height_ratio = key_height_ratio
        self.sensitivity = sensitivity

        self.keys: list[dict] = []
        self.active_keys: set[str] = set()
        self.playing_notes: set[str] = set()
        self.finger_history: dict[int, list[int]] = {}
        self.STRIKE_THRESHOLD = 15
        self.HISTORY_SIZE = 3
        # Structure d'une octave standard : C, D, E, F, G, A, B
        self.WHITE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
        
        # Pour le mode papier
        self.paper_quad: np.ndarray | None = None # Coordonnées des 4 coins de la feuille
        self.M: np.ndarray | None = None # Matrice de transformation de perspective
        self.M_inv: np.ndarray | None = None # Matrice inverse pour projeter les doigts sur la feuille
        self.calibration_cooldown = 0
        self.is_calibrated = False
        self.current_melody: list[str] = []
        self.melody_index: int = 0
        self.target_note: str | None = None
        self.score: int = 0
        self.combo: int = 0
        self.last_pressed_key: str | None = None
        self.last_press_time: float = 0.0
        self.press_cooldown: float = 0.1

    def _detect_paper(self, frame: np.ndarray) -> bool:
        """Détecte le contour rectangulaire de la feuille A4."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 75, 200)
        
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            
            if len(approx) == 4:
                # Vérifier si l'aire est suffisante
                if cv2.contourArea(approx) > (frame.shape[0] * frame.shape[1] * 0.1):
                    self.paper_quad = approx.reshape(4, 2)
                    return True
        return False

    def update_layout(self, frame_width: int, frame_height: int) -> None:
        self.keys.clear()
        
        # Si Desk View est activé, on simule une feuille A4 qui occupe le centre de l'image
        if self.app.current_mode == "paper_mode" and self.app.settings.get("is_desk_view"):
            self.is_calibrated = True
            margin_w = int(frame_width * 0.05)
            margin_h = int(frame_height * 0.05)
            self.paper_quad = np.array([
                [margin_w, margin_h], 
                [frame_width - margin_w, margin_h], 
                [frame_width - margin_w, frame_height - margin_h], 
                [margin_w, frame_height - margin_h]
            ])

        if self.app.current_mode == "paper_mode" and self.is_calibrated and self.paper_quad is not None:
            num_white = 14
            paper_w, paper_h = 1000, 700
            white_w = paper_w // num_white
            key_h = int(paper_h * 0.8)
            
            # Points sources (clavier virtuel plat)
            src_pts = np.float32([[0, 0], [paper_w, 0], [paper_w, paper_h], [0, paper_h]])
            
            # Points destination ordonnés
            dst_pts = self._order_points(self.paper_quad)
            
            # Gérer la rotation si nécessaire
            if self.app.settings.get("is_rotated"):
                # Inverser l'ordre des points destination pour une rotation à 180°
                dst_pts = np.roll(dst_pts, 2, axis=0)

            self.M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            self.M_inv = cv2.getPerspectiveTransform(dst_pts, src_pts)
            
            # Générer les touches en coordonnées "papier" (0-1000)
            for i in range(num_white):
                x = i * white_w
                note = self.WHITE_NOTES[i % 7]
                self.keys.append({
                    "id": f"white_{i}",
                    "paper_bbox": (x, 0, x + white_w, key_h),
                    "note": note, "octave": 4 + (i // 7), "color": (255, 255, 255), "type": "white"
                })
                # Touches noires
                if note in ["C", "D", "F", "G", "A"]:
                    bx = x + int(white_w * 0.7)
                    self.keys.append({
                        "id": f"black_{i}",
                        "paper_bbox": (bx, 0, bx + int(white_w * 0.6), int(key_h * 0.6)),
                        "note": note + "#", "octave": 4 + (i // 7), "color": (0, 0, 0), "type": "black"
                    })
            return

        # Mode Standard
        available_width = int(frame_width * 0.95)
        white_key_width = available_width // self.num_keys
        total_piano_width = white_key_width * self.num_keys
        offset_x = (frame_width - total_piano_width) // 2
        piano_height = int(frame_height * self.piano_height_ratio)
        key_height = int(piano_height * self.key_height_ratio)
        piano_y = 0

        for i in range(self.num_keys):
            x = offset_x + (i * white_key_width)
            note = self.WHITE_NOTES[i % 7]
            octave = 3 + (i // 7)
            self.keys.append({
                "id": f"white_{i}",
                "bbox": (x, piano_y, x + white_key_width, piano_y + key_height),
                "note": note, "octave": octave, "color": (255, 255, 255), "type": "white"
            })

        # 2. Générer les touches noires (C#, D#, F#, G#, A#)
        black_key_width = int(white_key_width * 0.6)
        black_key_height = int(key_height * 0.6)
        
        # Les touches noires sont placées entre les touches blanches
        # C# est entre C et D, D# entre D et E, etc.
        for i in range(self.num_keys - 1):
            current_white = self.WHITE_NOTES[i % 7]
            next_white = self.WHITE_NOTES[(i + 1) % 7]
            
            black_note = None
            if current_white == "C" and next_white == "D": black_note = "C#"
            elif current_white == "D" and next_white == "E": black_note = "D#"
            elif current_white == "F" and next_white == "G": black_note = "F#"
            elif current_white == "G" and next_white == "A": black_note = "G#"
            elif current_white == "A" and next_white == "B": black_note = "A#"
            
            if black_note:
                # Centre de la séparation entre les deux touches blanches (en tenant compte de l'offset)
                center_x = offset_x + (i + 1) * white_key_width
                x1 = center_x - (black_key_width // 2)
                octave = 3 + (i // 7)
                self.keys.append({
                    "id": f"black_{i}",
                    "bbox": (x1, piano_y, x1 + black_key_width, piano_y + black_key_height),
                    "note": black_note,
                    "octave": octave,
                    "color": (0, 0, 0),
                    "type": "black"
                })

    def _order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def check_press(self, finger_tips: list[tuple[int, int, int, float]]) -> None:
        current_time = time.time()
        touched_ids_this_frame: set[str] = set()
        is_paper = self.app.current_mode == "paper_mode" and self.is_calibrated and self.M_inv is not None

        sorted_keys = sorted(self.keys, key=lambda k: k["type"] == "white")

        for tip_id, tip_x, tip_y, tip_z in finger_tips:
            # En mode papier, on projette les coordonnées du doigt sur le plan de la feuille
            if is_paper:
                point = np.array([[[tip_x, tip_y]]], dtype=np.float32)
                transformed = cv2.perspectiveTransform(point, self.M_inv)
                px, py = transformed[0][0]
                # En mode papier, on est plus strict sur la détection de "frappe"
                # On peut utiliser la coordonnée Z de MediaPipe pour aider
            else:
                px, py = tip_x, tip_y

            if tip_id not in self.finger_history: self.finger_history[tip_id] = []
            self.finger_history[tip_id].append(py)
            if len(self.finger_history[tip_id]) > self.HISTORY_SIZE: self.finger_history[tip_id].pop(0)

            velocity = 0
            if len(self.finger_history[tip_id]) >= 2:
                velocity = self.finger_history[tip_id][-1] - self.finger_history[tip_id][0]

            for key in sorted_keys:
                if is_paper:
                    x1, y1, x2, y2 = key["paper_bbox"]
                else:
                    x1, y1, x2, y2 = key["bbox"]
                
                if x1 < px < x2 and y1 < py < y2:
                    touched_ids_this_frame.add(key["id"])
                    
                    # En mode papier, on combine vélocité Y et profondeur Z pour détecter le "tap"
                    # tip_z < -0.05 signifie souvent que le doigt est plus proche de la caméra (en train d'appuyer)
                    strike_detected = False
                    if is_paper:
                        # Seuil de vélocité plus faible car le mouvement est plus court sur papier
                        if velocity > (self.STRIKE_THRESHOLD * 0.5) and tip_z < -0.02:
                            strike_detected = True
                    else:
                        if velocity > self.STRIKE_THRESHOLD:
                            strike_detected = True

                    if strike_detected and key["id"] not in self.playing_notes:
                        self.playing_notes.add(key["id"])
                        # Utiliser l'octave stockée dans la touche
                        self.app.sound_player.play_note(key["note"], key.get("octave", 4))
                        
                        # LOGIQUE DE LEÇON : On compare la note jouée à la note cible
                        if self.app.current_mode == "lesson" and self.target_note:
                            if key["note"] == self.target_note:
                                self.score += 1 + self.combo
                                self.combo += 1
                                self.app.update_score_display()
                                self.app.next_note()
                            else:
                                self.combo = 0
                                self.app.update_score_display()
                        
                        self.last_pressed_key = key["note"]
                        self.last_press_time = current_time
                    break

        # Mise à jour de l'état visuel (active_keys)
        self.active_keys = touched_ids_this_frame

        # Nettoyer playing_notes : une note peut être rejouée si le doigt quitte la touche ou remonte
        for kid in list(self.playing_notes):
            if kid not in touched_ids_this_frame:
                self.playing_notes.remove(kid)
            else:
                # Si le doigt est toujours sur la touche mais remonte, on permet de re-frapper
                # (Optionnel : nécessite de vérifier la vélocité négative)
                pass

        # Nettoyer l'historique des doigts disparus
        active_tip_ids = [t[0] for t in finger_tips]
        for tid in list(self.finger_history.keys()):
            if tid not in active_tip_ids: del self.finger_history[tid]

    def draw(self, frame: np.ndarray) -> None:
        is_paper = self.app.current_mode == "paper_mode"
        
        if is_paper and self.M is not None:
            # En mode papier calibré, on dessine chaque touche transformée par la perspective
            for key in self.keys:
                x1, y1, x2, y2 = key["paper_bbox"]
                # Créer les 4 coins de la touche
                pts = np.float32([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]).reshape(-1, 1, 2)
                # Transformer les coins vers l'image caméra
                transformed_pts = cv2.perspectiveTransform(pts, self.M).reshape(-1, 2).astype(np.int32)
                
                color = (173, 216, 230) if key["id"] in self.active_keys else key["color"]
                if self.app.current_mode == "lesson" and key["note"] == self.target_note:
                    color = (144, 238, 144)
                
                # Dessiner le polygone rempli avec transparence
                overlay = frame.copy()
                cv2.fillPoly(overlay, [transformed_pts], color)
                cv2.polylines(overlay, [transformed_pts], True, (80, 80, 80), 2)
                
                # Label au centre de la touche
                center = np.mean(transformed_pts, axis=0).astype(np.int32)
                cv2.putText(frame, key["note"], (center[0]-10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                
                cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            return

        # Mode Standard
        overlay = frame.copy()
        for key in self.keys:
            x1, y1, x2, y2 = key["bbox"]
            color = (173, 216, 230) if key["id"] in self.active_keys else key["color"]
            if self.app.current_mode == "lesson" and key["note"] == self.target_note:
                color = (144, 238, 144)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (80, 80, 80), 1)
            cv2.putText(overlay, key["note"], (x1 + 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        np.copyto(frame, overlay)


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE : PianoApp
# ─────────────────────────────────────────────────────────────────────────────
class PianoApp(ctk.CTk):
    DEFAULT_SETTINGS = {
        "piano_height_ratio": 0.3,
        "key_width_ratio": 0.07,
        "key_height_ratio": 0.6,
        "sensitivity": 0.6,
        "num_keys": 14,
        "language": "FR",
        "camera_index": 0,
        "is_desk_view": False,
        "is_rotated": False
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("iPiano")
        self.geometry("1280x720")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Raccourcis clavier
        self.bind("<r>", lambda e: self.show_landing())
        self.bind("<R>", lambda e: self.show_landing())
        self.bind("<q>", lambda e: self._on_closing())
        self.bind("<Q>", lambda e: self._on_closing())
        self.bind("<v>", lambda e: self._cycle_camera())
        self.bind("<V>", lambda e: self._cycle_camera())

        self.current_mode: str = "landing"
        self.current_language: str = self.DEFAULT_SETTINGS["language"]
        self.settings = self.DEFAULT_SETTINGS.copy()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erreur: Impossible d'ouvrir la webcam.")
            sys.exit(1)

        self.tracker = HandTracker()
        self.sound_player = SoundPlayer()
        self.piano = VirtualPiano(self, **self.settings)

        self.video_frame = ctk.CTkLabel(self, text="")
        self.video_frame.pack(fill="both", expand=True)

        self._build_landing()
        self._build_lesson()
        self._build_settings()

        self.show_landing()

        self.video_thread = threading.Thread(target=self._video_loop, daemon=True)
        self.video_thread.start()

    def _on_closing(self) -> None:
        self.cap.release()
        self.tracker.close()
        self.sound_player.close()
        self.destroy()

    def t(self, key: str) -> str: return TRANSLATIONS[self.current_language].get(key, key)

    def _build_landing(self) -> None:
        self.landing_frame = ctk.CTkFrame(self, corner_radius=28, fg_color="#F2F2F7")
        # Ne pas placer ici, show_landing s'en occupe

        ctk.CTkLabel(self.landing_frame, text=self.t("title"), font=ctk.CTkFont(family="Helvetica Neue", size=60, weight="bold")).pack(pady=(50, 10))
        ctk.CTkLabel(self.landing_frame, text=self.t("subtitle"), font=ctk.CTkFont(family="Helvetica Neue", size=20, slant="italic")).pack(pady=10)

        ctk.CTkButton(self.landing_frame, text=self.t("start_lesson"), command=self.show_lesson, font=ctk.CTkFont(family="Helvetica Neue", size=20, weight="bold"), fg_color="#007AFF", hover_color="#0056B3", height=50, corner_radius=15).pack(pady=(40, 10), ipadx=30)
        ctk.CTkButton(self.landing_frame, text=self.t("free_play"), command=self.start_free_play, font=ctk.CTkFont(family="Helvetica Neue", size=20, weight="bold"), fg_color="#34C759", hover_color="#28A745", height=50, corner_radius=15).pack(pady=10, ipadx=30)
        ctk.CTkButton(self.landing_frame, text=self.t("settings"), command=self.show_settings, font=ctk.CTkFont(family="Helvetica Neue", size=20), fg_color="#FF9500", hover_color="#CC7A00", height=50, corner_radius=15).pack(pady=10, ipadx=30)
        ctk.CTkButton(self.landing_frame, text=self.t("paper_mode"), command=self.start_paper_mode, font=ctk.CTkFont(family="Helvetica Neue", size=20, weight="bold"), fg_color="#5856D6", hover_color="#4342A5", height=50, corner_radius=15).pack(pady=10, ipadx=30)

    def _build_lesson(self) -> None:
        self.lesson_frame = ctk.CTkFrame(self, corner_radius=28, fg_color="#F2F2F7")
        # Ne pas placer ici, show_lesson s'en occupe

        top_bar = ctk.CTkFrame(self.lesson_frame, fg_color="transparent")
        top_bar.pack(pady=10, fill="x", padx=20)

        self.score_label = ctk.CTkLabel(top_bar, text=f"{self.t('score')}: 0", font=ctk.CTkFont(family="Helvetica Neue", size=16, weight="bold"))
        self.score_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(top_bar, width=200, height=10, corner_radius=5, fg_color="#E5E5EA", progress_color="#007AFF")
        self.progress_bar.set(0)
        self.progress_bar.pack(side="right", padx=(0, 10))

        self.progress_label = ctk.CTkLabel(top_bar, text=f"{self.t('progression')}: 0/0", font=ctk.CTkFont(family="Helvetica Neue", size=13, slant="italic"))
        self.progress_label.pack(side="right")

        ctk.CTkLabel(self.lesson_frame, text=self.t("choose_melody"), font=ctk.CTkFont(family="Helvetica Neue", size=18, weight="bold")).pack(pady=(20, 5))
        self.melody_selector = ctk.CTkOptionMenu(self.lesson_frame, values=list(MELODIES.keys()), command=self._select_melody, font=ctk.CTkFont(family="Helvetica Neue", size=16), fg_color="#E5E5EA", button_color="#007AFF", button_hover_color="#0056B3", dropdown_fg_color="#F2F2F7", dropdown_hover_color="#D1D1D6")
        self.melody_selector.pack(pady=10)

        self.target_note_label = ctk.CTkLabel(self.lesson_frame, text="", font=ctk.CTkFont(family="Helvetica Neue", size=40, weight="bold"), text_color="#007AFF")
        self.target_note_label.pack(pady=30)

        ctk.CTkButton(self.lesson_frame, text=self.t("back"), command=self.show_landing, font=ctk.CTkFont(family="Helvetica Neue", size=18), fg_color="#FF3B30", hover_color="#CC2D2D", height=40, corner_radius=15).pack(pady=20, ipadx=20)

    def _build_settings(self) -> None:
        self.settings_frame = ctk.CTkFrame(self, corner_radius=28, fg_color="#F2F2F7")
        # Ne pas placer ici, show_settings s'en occupe

        ctk.CTkLabel(self.settings_frame, text=self.t("settings"), font=ctk.CTkFont(family="Helvetica Neue", size=30, weight="bold")).pack(pady=(30, 20))

        lang_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        lang_frame.pack(pady=5)
        ctk.CTkLabel(lang_frame, text=self.t("language"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.lang_selector = ctk.CTkOptionMenu(lang_frame, values=list(TRANSLATIONS.keys()), command=self._change_language, font=ctk.CTkFont(family="Helvetica Neue", size=16), fg_color="#E5E5EA", button_color="#007AFF", button_hover_color="#0056B3", dropdown_fg_color="#F2F2F7", dropdown_hover_color="#D1D1D6")
        self.lang_selector.set(self.current_language)
        self.lang_selector.pack(side="right", padx=10)

        height_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        height_frame.pack(pady=5)
        ctk.CTkLabel(height_frame, text=self.t("height"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.height_slider = ctk.CTkSlider(height_frame, from_=0.1, to=0.5, number_of_steps=40, command=self._update_piano_settings, fg_color="#E5E5EA", progress_color="#007AFF")
        self.height_slider.set(self.settings["piano_height_ratio"])
        self.height_slider.pack(side="right", padx=10)

        width_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        width_frame.pack(pady=5)
        ctk.CTkLabel(width_frame, text=self.t("width"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.width_slider = ctk.CTkSlider(width_frame, from_=0.05, to=0.1, number_of_steps=50, command=self._update_piano_settings, fg_color="#E5E5EA", progress_color="#007AFF")
        self.width_slider.set(self.settings["key_width_ratio"])
        self.width_slider.pack(side="right", padx=10)

        key_height_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        key_height_frame.pack(pady=5)
        ctk.CTkLabel(key_height_frame, text=self.t("key_height"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.key_height_slider = ctk.CTkSlider(key_height_frame, from_=0.4, to=0.9, number_of_steps=50, command=self._update_piano_settings, fg_color="#E5E5EA", progress_color="#007AFF")
        self.key_height_slider.set(self.settings["key_height_ratio"])
        self.key_height_slider.pack(side="right", padx=10)

        sensitivity_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        sensitivity_frame.pack(pady=5)
        ctk.CTkLabel(sensitivity_frame, text=self.t("sensitivity"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.sensitivity_slider = ctk.CTkSlider(sensitivity_frame, from_=0.1, to=1.0, number_of_steps=90, command=self._update_piano_settings, fg_color="#E5E5EA", progress_color="#007AFF")
        self.sensitivity_slider.set(self.settings["sensitivity"])
        self.sensitivity_slider.pack(side="right", padx=10)

        num_keys_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        num_keys_frame.pack(pady=5)
        ctk.CTkLabel(num_keys_frame, text=self.t("num_keys"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left", padx=10)
        self.num_keys_slider = ctk.CTkSlider(num_keys_frame, from_=7, to=21, number_of_steps=14, command=self._update_piano_settings, fg_color="#E5E5EA", progress_color="#007AFF")
        self.num_keys_slider.set(self.settings["num_keys"])
        self.num_keys_slider.pack(side="right", padx=10)

        # Caméra & Desk View
        camera_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        camera_frame.pack(pady=5, fill="x", padx=40)
        ctk.CTkLabel(camera_frame, text=self.t("camera_source"), font=ctk.CTkFont(family="Helvetica Neue", size=16)).pack(side="left")
        self.camera_option = ctk.CTkOptionMenu(camera_frame, values=["0", "1", "2"], command=self._change_camera, font=ctk.CTkFont(family="Helvetica Neue", size=14))
        self.camera_option.set(str(self.settings["camera_index"]))
        self.camera_option.pack(side="right")

        self.desk_view_switch = ctk.CTkSwitch(self.settings_frame, text=self.t("desk_view"), command=self._toggle_desk_view, font=ctk.CTkFont(family="Helvetica Neue", size=16), progress_color="#007AFF")
        self.desk_view_switch.pack(pady=5)
        if self.settings["is_desk_view"]: self.desk_view_switch.select()

        self.rotate_switch = ctk.CTkSwitch(self.settings_frame, text=self.t("rotate_piano"), command=self._toggle_rotation, font=ctk.CTkFont(family="Helvetica Neue", size=16), progress_color="#007AFF")
        self.rotate_switch.pack(pady=5)
        if self.settings.get("is_rotated"): self.rotate_switch.select()

        ctk.CTkButton(self.settings_frame, text=self.t("download_template"), command=self._download_template, font=ctk.CTkFont(family="Helvetica Neue", size=18), fg_color="#007AFF", hover_color="#0056B3", height=40, corner_radius=15).pack(pady=(10, 10), ipadx=20)
        ctk.CTkButton(self.settings_frame, text=self.t("reset"), command=self._reset_settings, font=ctk.CTkFont(family="Helvetica Neue", size=18), fg_color="#FF3B30", hover_color="#CC2D2D", height=40, corner_radius=15).pack(pady=10, ipadx=20)
        ctk.CTkButton(self.settings_frame, text=self.t("back"), command=self.show_landing, font=ctk.CTkFont(family="Helvetica Neue", size=18), fg_color="#FF9500", hover_color="#CC7A00", height=40, corner_radius=15).pack(pady=10, ipadx=20)

    def _update_piano_settings(self, value: float) -> None:
        self.settings["piano_height_ratio"] = self.height_slider.get()
        self.settings["key_width_ratio"] = self.width_slider.get()
        self.settings["key_height_ratio"] = self.key_height_slider.get()
        self.settings["sensitivity"] = self.sensitivity_slider.get()
        self.settings["num_keys"] = int(self.num_keys_slider.get())
        self.piano.num_keys = self.settings["num_keys"]
        self.piano.piano_height_ratio = self.settings["piano_height_ratio"]
        self.piano.key_width_ratio = self.settings["key_width_ratio"]
        self.piano.key_height_ratio = self.settings["key_height_ratio"]
        self.piano.sensitivity = self.settings["sensitivity"]

    def _reset_settings(self) -> None:
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.current_language = self.DEFAULT_SETTINGS["language"]
        self.lang_selector.set(self.current_language)
        self.height_slider.set(self.settings["piano_height_ratio"])
        self.width_slider.set(self.settings["key_width_ratio"])
        self.key_height_slider.set(self.settings["key_height_ratio"])
        self.sensitivity_slider.set(self.settings["sensitivity"])
        self.num_keys_slider.set(self.settings["num_keys"])
        self._update_piano_settings(0)
        self._update_ui_texts()

    def _change_language(self, new_lang: str) -> None:
        self.current_language = new_lang
        self._update_ui_texts()

    def _change_camera(self, index: str) -> None:
        idx = int(index)
        if idx != self.settings["camera_index"]:
            self.settings["camera_index"] = idx
            self.cap.release()
            self.cap = cv2.VideoCapture(idx)

    def _toggle_desk_view(self) -> None:
        self.settings["is_desk_view"] = self.desk_view_switch.get() == 1
        self.piano.is_calibrated = False

    def _toggle_rotation(self) -> None:
        self.settings["is_rotated"] = self.rotate_switch.get() == 1
        self.piano.is_calibrated = False

    def _cycle_camera(self) -> None:
        """Bascule entre les caméras 0, 1 et 2."""
        new_idx = (self.settings["camera_index"] + 1) % 3
        self._change_camera(str(new_idx))
        self.camera_option.set(str(new_idx))

    def _update_ui_texts(self) -> None:
        self.landing_frame.winfo_children()[0].configure(text=self.t("title"))
        self.landing_frame.winfo_children()[1].configure(text=self.t("subtitle"))
        self.landing_frame.winfo_children()[2].configure(text=self.t("start_lesson"))
        self.landing_frame.winfo_children()[3].configure(text=self.t("free_play"))
        self.landing_frame.winfo_children()[4].configure(text=self.t("settings"))
        self.landing_frame.winfo_children()[5].configure(text=self.t("paper_mode"))

        self.score_label.configure(text=f"{self.t('score')}: {self.piano.score}")
        self.progress_label.configure(text=f"{self.t('progression')}: {self.piano.melody_index}/{len(self.piano.current_melody)}")
        self.lesson_frame.winfo_children()[1].configure(text=self.t("choose_melody"))
        self.lesson_frame.winfo_children()[4].configure(text=self.t("back"))
        
        # Mettre à jour les labels des réglages
        # (C'est un peu fragile de se baser sur l'index des enfants, mais cohérent avec le code existant)
        self.settings_frame.winfo_children()[0].configure(text=self.t("settings"))
        self.settings_frame.winfo_children()[8].configure(text=self.t("download_template"))
        self.settings_frame.winfo_children()[9].configure(text=self.t("reset"))
        self.settings_frame.winfo_children()[10].configure(text=self.t("back"))

        self.settings_frame.winfo_children()[0].configure(text=self.t("settings"))
        self.settings_frame.winfo_children()[1].winfo_children()[0].configure(text=self.t("language"))
        self.settings_frame.winfo_children()[2].winfo_children()[0].configure(text=self.t("height"))
        self.settings_frame.winfo_children()[3].winfo_children()[0].configure(text=self.t("width"))
        self.settings_frame.winfo_children()[4].winfo_children()[0].configure(text=self.t("key_height"))
        self.settings_frame.winfo_children()[5].winfo_children()[0].configure(text=self.t("sensitivity"))
        self.settings_frame.winfo_children()[6].winfo_children()[0].configure(text=self.t("num_keys"))
        self.settings_frame.winfo_children()[7].configure(text=self.t("reset"))
        self.settings_frame.winfo_children()[8].configure(text=self.t("back"))

    def show_landing(self) -> None:
        self.current_mode = "landing"
        self.piano.is_calibrated = False # Reset calibration
        self.lesson_frame.place_forget()
        self.settings_frame.place_forget()
        self.landing_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)
        self.landing_frame.lift()

    def show_lesson(self) -> None:
        self.current_mode = "lesson"
        self.piano.score = 0
        self.piano.combo = 0
        self.piano.melody_index = 0
        self.piano.current_melody = []
        self.piano.target_note = None
        self.update_score_display()
        self.landing_frame.place_forget()
        self.settings_frame.place_forget()
        self.lesson_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)
        self.lesson_frame.lift()
        # On affiche le sélecteur de mélodie au début
        for child in self.lesson_frame.winfo_children():
            child.pack()

    def start_free_play(self) -> None:
        self.current_mode = "free_play"
        self.piano.score = 0
        self.piano.combo = 0
        self.piano.melody_index = 0
        self.piano.current_melody = []
        self.piano.target_note = None
        self.update_score_display()
        self.landing_frame.place_forget()
        self.settings_frame.place_forget()
        self.lesson_frame.place_forget() # On cache tout pour le mode libre
        self.target_note_label.configure(text=self.t("free_play_title"))

    def start_paper_mode(self) -> None:
        self.current_mode = "paper_mode"
        
        # Automatisation Desk View : Tenter de passer sur la caméra 1 si Desk View est activé
        if self.settings.get("is_desk_view") and self.settings["camera_index"] == 0:
            self._change_camera("1")
            
        self.piano.score = 0
        self.piano.combo = 0
        self.piano.melody_index = 0
        self.piano.current_melody = []
        self.piano.target_note = None
        self.update_score_display()
        self.landing_frame.place_forget()
        self.settings_frame.place_forget()
        self.lesson_frame.place_forget()
        # En mode papier, on change un peu les paramètres par défaut du piano pour coller à la feuille
        self.piano.piano_height_ratio = 0.5
        self.piano.key_height_ratio = 0.8
        self.target_note_label.configure(text=self.t("paper_mode"))

    def _download_template(self) -> None:
        # Sur un vrai système, on ouvrirait une boîte de dialogue de sauvegarde.
        # Ici, on va s'assurer que le fichier est présent et informer l'utilisateur.
        template_path = os.path.join(os.path.dirname(__file__), "piano_template_a4.png")
        if os.path.exists(template_path):
            import shutil
            # On simule un "téléchargement" en le copiant sur le bureau de l'utilisateur s'il existe
            desktop = os.path.expanduser("~/Desktop")
            if os.path.exists(desktop):
                try:
                    shutil.copy(template_path, os.path.join(desktop, "piano_template_a4.png"))
                    print(f"Template copié sur le bureau : {desktop}")
                except: pass
            
            # Ouvrir le fichier avec l'application par défaut du système
            try:
                if sys.platform == "win32": os.startfile(template_path)
                elif sys.platform == "darwin": os.system(f"open '{template_path}'")
                else: os.system(f"xdg-open '{template_path}'")
            except: pass

    def show_settings(self) -> None:
        self.current_mode = "settings"
        self.landing_frame.place_forget()
        self.lesson_frame.place_forget()
        self.settings_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)
        self.settings_frame.lift()

    def _select_melody(self, melody_name: str) -> None:
        self.piano.current_melody = MELODIES.get(melody_name, [])
        self.piano.melody_index = 0
        self.piano.score = 0
        self.piano.combo = 0
        self.update_score_display()
        self.next_note()
        # Cacher le sélecteur une fois la mélodie choisie pour voir le piano
        self.lesson_frame.place_forget()

    def next_note(self) -> None:
        if self.piano.melody_index < len(self.piano.current_melody):
            self.piano.target_note = self.piano.current_melody[self.piano.melody_index]
            self.target_note_label.configure(text=f"{self.t('play_note')} {self.piano.target_note}")
            self.piano.melody_index += 1
            self.progress_bar.set(self.piano.melody_index / len(self.piano.current_melody))
            self.progress_label.configure(text=f"{self.t('progression')}: {self.piano.melody_index}/{len(self.piano.current_melody)}")
        else:
            self.piano.target_note = None
            self.target_note_label.configure(text=self.t("finished"))
            self.progress_bar.set(1)
            self.progress_label.configure(text=f"{self.t('progression')}: {len(self.piano.current_melody)}/{len(self.piano.current_melody)}")

    def update_score_display(self) -> None:
        score_text = f"{self.t('score')}: {self.piano.score}"
        if self.piano.combo > 1: score_text += f" (x{self.piano.combo} Combo!)"
        self.score_label.configure(text=score_text)

    def _video_loop(self) -> None:
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            # En mode Desk View, on ne flippe pas l'image car c'est une vue de dessus réelle
            if not self.settings.get("is_desk_view"):
                frame = cv2.flip(frame, 1)
                
            frame_height, frame_width, _ = frame.shape

            hand_mask = self.tracker.process_frame(frame.copy(), draw=False)
            finger_tips = self.tracker.get_finger_tips(frame)

            if self.current_mode == "paper_mode" and not self.piano.is_calibrated and not self.settings.get("is_desk_view"):
                # Tenter de détecter la feuille pour calibrer (seulement si pas en Desk View)
                if self.piano._detect_paper(frame):
                    self.piano.is_calibrated = True
                else:
                    cv2.putText(frame, "Veuillez presenter la feuille A4...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            self.piano.update_layout(frame_width, frame_height)

            display_frame = frame.copy()
            self.piano.draw(display_frame)

            hand_pixels = cv2.bitwise_and(frame, frame, mask=hand_mask)
            display_frame = np.where(hand_mask[:, :, None] == 255, hand_pixels, display_frame)

            self.tracker.draw_landmarks(display_frame)

            if self.current_mode in ["lesson", "free_play", "paper_mode"]:
                self.piano.check_press(finger_tips)

            img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

            self.update_idletasks()
            time.sleep(0.016)


if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur: Le modèle MediaPipe 'hand_landmarker.task' est manquant à {MODEL_PATH}")
        sys.exit(1)

    app = PianoApp()
    app.mainloop()