import math
from stored_gestures import raw_gesture_templates

class DollarRecognizer:

    N_RESAMPLE_POINTS = 64

    def __init__(self, points):
        self.raw_gesture_templates = raw_gesture_templates
        self.points = points
    
    def compute_centroid(self):
        centroid_x = sum(point[0] for point in self.points) / self.N_RESAMPLE_POINTS
        centroid_y = sum(point[1] for point in self.points) / self.N_RESAMPLE_POINTS

        return (centroid_x, centroid_y)

    def indicative_angle(self):
        centroid_x, centroid_y = self.compute_centroid()

        return math.atan2(centroid_y - self.points[0][1], centroid_x - self.points[0][0])

    def rotate_by(self, omega):
        centroid_x, centroid_y = self.compute_centroid()
        rotated_points = []

        for point in self.points:
            q_x = point[0] - centroid_x
            q_y = point[1] - centroid_y
            rotated_x = q_x * math.cos(omega) - q_y * math.sin(omega) + centroid_x
            rotated_y = q_x * math.sin(omega) + q_y * math.cos(omega) + centroid_y
            rotated_points.append(rotated_x, rotated_y)

        return rotated_points

    def scale_to(self, size):
        min_x = min(point[0] for point in self.points)
        min_y = min(point[1] for point in self.points)
        max_x = max(point[0] for point in self.points)
        max_y = max(point[1] for point in self.points)
        b_width = max_x - min_x
        b_height = max_y - min_y

        scaled_points = []

        for point in self.points:
            q_x = point[0] * size / b_width
            q_y = point[1] * size / b_height
            scaled_points.append((q_x, q_y))

        return scaled_points

    def translate_to(self, k):
        centroid_x, centroid_y = self.compute_centroid()

        translated_points = []

        for point in self.points:
            q_x = point[0] + k[0] - centroid_x
            q_y = point[1] + k[1] - centroid_y
            translated_points.append((q_x, q_y))
        
        return translated_points