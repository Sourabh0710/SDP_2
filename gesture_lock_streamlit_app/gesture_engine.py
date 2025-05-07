import numpy as np
import pickle
import os
from cryptography.fernet import Fernet
from sklearn.neighbors import KNeighborsClassifier

class GestureEngine:
    def __init__(self):
        self.key_path = "key.key"
        self.data_path = "patterns.dat"
        self.log_path = "unlock_attempts.log"
        self._load_or_generate_key()

    def _load_or_generate_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(key)
        with open(self.key_path, 'rb') as f:
            self.cipher = Fernet(f.read())

    def save_pattern(self, points):
        vector = self._vectorize(points)
        encrypted = self.cipher.encrypt(pickle.dumps(vector))
        with open(self.data_path, 'wb') as f:
            f.write(encrypted)

    def load_pattern(self):
        if not os.path.exists(self.data_path):
            return None
        with open(self.data_path, 'rb') as f:
            decrypted = self.cipher.decrypt(f.read())
        return pickle.loads(decrypted)

    def _vectorize(self, points, num=64):
        points = np.array(points)
        if len(points) < 2:
            return np.zeros((num, 2)).flatten()
        distances = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
        distances = np.insert(distances, 0, 0)
        resampled = np.zeros((num, 2))
        for i in range(2):
            resampled[:, i] = np.interp(
                np.linspace(0, distances[-1], num), distances, points[:, i]
            )
        return resampled.flatten()

    def is_match(self, ref_points, test_points, tolerance=0.15):
        vec1 = self._vectorize(ref_points)
        vec2 = self._vectorize(test_points)
        distance = np.linalg.norm(vec1 - vec2)
        return distance < tolerance * np.linalg.norm(vec1)
