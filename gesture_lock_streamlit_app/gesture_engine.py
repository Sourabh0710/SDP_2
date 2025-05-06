import numpy as np
import pickle, os, base64
from cryptography.fernet import Fernet
from sklearn.neighbors import KNeighborsClassifier

class GestureEngine:
    def __init__(self):
        self.patterns = []
        self._load_or_generate_key()
        self.classifier = KNeighborsClassifier(n_neighbors=1)

    def _load_or_generate_key(self):
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as f:
                f.write(key)
        with open("key.key", "rb") as f:
            self.cipher = Fernet(f.read())

    def resample(self, points, num_points=64):
        if len(points) < 2:
            return np.zeros((num_points, 2))
        points = np.array(points)
        distances = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1)))
        distances = np.insert(distances, 0, 0)
        uniform_dist = np.linspace(0, distances[-1], num_points)
        return np.vstack([np.interp(uniform_dist, distances, points[:, i]) for i in range(2)]).T

    def compare_patterns(self, pattern1, pattern2):
        p1 = self.resample(pattern1)
        p2 = self.resample(pattern2)
        return np.linalg.norm(p1 - p2) < 1000  # Tolerance

    def save_pattern(self, points):
        resampled = self.resample(points)
        data = pickle.dumps(resampled)
        encrypted = self.cipher.encrypt(data)
        with open("patterns.dat", "wb") as f:
            f.write(encrypted)
        with open("unlock_attempts.log", "a") as log:
            log.write("Pattern saved
")