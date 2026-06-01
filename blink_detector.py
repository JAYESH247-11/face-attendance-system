import cv2
import mediapipe as mp
import numpy as np


class BlinkDetector:

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    EAR_THRESHOLD = 0.21
    MIN_CLOSED_FRAMES = 2
    REQUIRED_BLINKS = 1

    def __init__(self):


        self.blink_count = 0
        self.closed_frames = 0
        self.ear_history = []
        self.verified = False

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def reset(self):

        self.blink_count = 0
        self.closed_frames = 0
        self.ear_history.clear()
        self.verified = False

    def euclidean(self, p1, p2):

        return np.linalg.norm(
            np.array(p1) - np.array(p2)
        )

    def calculate_ear(self, landmarks, eye_points):

        p1 = landmarks[eye_points[0]]
        p2 = landmarks[eye_points[1]]
        p3 = landmarks[eye_points[2]]
        p4 = landmarks[eye_points[3]]
        p5 = landmarks[eye_points[4]]
        p6 = landmarks[eye_points[5]]

        vertical1 = self.euclidean(p2, p6)
        vertical2 = self.euclidean(p3, p5)

        horizontal = self.euclidean(p1, p4)

        if horizontal == 0:
            return 0

        ear = (
            vertical1 + vertical2
        ) / (2.0 * horizontal)

        return ear

    def process(self, rgb):

        h, w, _ = rgb.shape

        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return False

        face = results.multi_face_landmarks[0]

        landmarks = []

        for lm in face.landmark:

            x = int(lm.x * w)
            y = int(lm.y * h)

            landmarks.append((x, y))

        left_ear = self.calculate_ear(
            landmarks,
            self.LEFT_EYE
        )

        right_ear = self.calculate_ear(
            landmarks,
            self.RIGHT_EYE
        )

        ear = (left_ear + right_ear) / 2

        self.ear_history.append(ear)

        if len(self.ear_history) > 5:
            self.ear_history.pop(0)

        ear = sum(self.ear_history) / len(self.ear_history)

        if ear < self.EAR_THRESHOLD:

            self.closed_frames += 1

        else:

            if (
                self.closed_frames
                >= self.MIN_CLOSED_FRAMES
            ):
                self.blink_count += 1

            self.closed_frames = 0

        if self.blink_count >= self.REQUIRED_BLINKS:

            self.verified = True
            return True

        return False