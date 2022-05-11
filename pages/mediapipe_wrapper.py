import cv2
import mediapipe as mp
import numpy as np

# filename = "/home/paxpan/Downloads/man-counting-five.jpg"
# image = cv2.flip(cv2.imread(filename), 1)

class MediapipeHolistic:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(static_image_mode=False)
        self.part_correspondence = {"WRIST": self.mp_holistic.HandLandmark.WRIST,
                               "THUMB_CMC": self.mp_holistic.HandLandmark.THUMB_CMC,
                               "THUMB_MCP": self.mp_holistic.HandLandmark.THUMB_MCP,
                               "THUMB_IP": self.mp_holistic.HandLandmark.THUMB_IP,
                               "THUMB_TIP": self.mp_holistic.HandLandmark.THUMB_TIP,
                               "INDEX_FINGER_MCP": self.mp_holistic.HandLandmark.INDEX_FINGER_MCP,
                               "INDEX_FINGER_PIP": self.mp_holistic.HandLandmark.INDEX_FINGER_PIP,
                               "INDEX_FINGER_DIP": self.mp_holistic.HandLandmark.INDEX_FINGER_DIP,
                               "INDEX_FINGER_TIP": self.mp_holistic.HandLandmark.INDEX_FINGER_TIP,
                               "MIDDLE_FINGER_MCP": self.mp_holistic.HandLandmark.MIDDLE_FINGER_MCP,
                               "MIDDLE_FINGER_PIP": self.mp_holistic.HandLandmark.MIDDLE_FINGER_PIP,
                               "MIDDLE_FINGER_DIP": self.mp_holistic.HandLandmark.MIDDLE_FINGER_DIP,
                               "MIDDLE_FINGER_TIP": self.mp_holistic.HandLandmark.MIDDLE_FINGER_TIP,
                               "RING_FINGER_MCP": self.mp_holistic.HandLandmark.RING_FINGER_MCP,
                               "RING_FINGER_PIP": self.mp_holistic.HandLandmark.RING_FINGER_PIP,
                               "RING_FINGER_DIP": self.mp_holistic.HandLandmark.RING_FINGER_DIP,
                               "RING_FINGER_TIP": self.mp_holistic.HandLandmark.RING_FINGER_TIP,
                               "PINKY_MCP": self.mp_holistic.HandLandmark.PINKY_MCP,
                               "PINKY_PIP": self.mp_holistic.HandLandmark.PINKY_PIP,
                               "PINKY_DIP": self.mp_holistic.HandLandmark.PINKY_DIP,
                               "PINKY_TIP": self.mp_holistic.HandLandmark.PINKY_TIP
                               }

    def process_image(self, image: np.ndarray):
        self.results_holistic = self.holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def there_is_left_hand(self):
        return self.results_holistic.left_hand_landmarks is not None

    def there_is_right_hand(self):
        return self.results_holistic.right_hand_landmarks is not None

    def get_hand_part(self, which_hand, which_part):
        if which_hand == "LEFT":
            if self.there_is_left_hand():
                x = self.results_holistic.left_hand_landmarks.landmark[self.part_correspondence[which_part]].x
                y = self.results_holistic.left_hand_landmarks.landmark[self.part_correspondence[which_part]].y
                z = self.results_holistic.left_hand_landmarks.landmark[self.part_correspondence[which_part]].z
                return x, y, z
            else:
                return None
        else:
            if self.there_is_right_hand():
                x = self.results_holistic.right_hand_landmarks.landmark[self.part_correspondence[which_part]].x
                y = self.results_holistic.right_hand_landmarks.landmark[self.part_correspondence[which_part]].y
                z = self.results_holistic.right_hand_landmarks.landmark[self.part_correspondence[which_part]].z
                return x, y, z
            else:
                return None

    def draw_marks(self, image: np.ndarray):
        annotated_image = image.copy()
        self.mp_drawing.draw_landmarks(
            annotated_image, self.results_holistic.face_landmarks, self.mp_holistic.FACE_CONNECTIONS)
        self.mp_drawing.draw_landmarks(
            annotated_image, self.results_holistic.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        self.mp_drawing.draw_landmarks(
            annotated_image, self.results_holistic.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        self.mp_drawing.draw_landmarks(
            annotated_image, self.results_holistic.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
        return annotated_image

    
    def landmarks_to_array(self, which_hand, flatten=True):
        num_joints = 21
        if which_hand == "LEFT" and self.there_is_left_hand():
            landmarks = self.results_holistic.left_hand_landmarks.landmark
        elif which_hand == "RIGHT" and self.there_is_right_hand():
            landmarks = self.results_holistic.right_hand_landmarks.landmark
        else:
            return None

        landmarks_now = np.empty(shape=(num_joints, 3))
        for idx, actual_landmark in enumerate(landmarks):
            landmarks_now[idx, 0] = actual_landmark.x
            landmarks_now[idx, 1] = actual_landmark.y
            landmarks_now[idx, 2] = actual_landmark.z

        if flatten:
            landmarks_now = landmarks_now.flatten('F')

        return landmarks_now

    def featurenames(self):
        names = list(self.part_correspondence.keys())
        coords = ['_X','_Y','_Z']
        names_new = [name+coord for coord in coords for name in names ]
        return names_new

