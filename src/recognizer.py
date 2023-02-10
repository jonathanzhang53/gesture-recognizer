import math
import json
from collections import defaultdict
from stored_gestures import raw_gesture_templates

class DollarRecognizer:
    N_RESAMPLE_POINTS = 64
    SIZE = 250

    def __init__(self, points):
        self.raw_gesture_templates = raw_gesture_templates
        self.preprocessed_gesture_templates = defaultdict(list) # hashmap of with key = gesture name and value = list of templates
        self.points = points
        # self.processTemplates()
        
    def processTemplates(self):
        for templateName, templatePoints in self.raw_gesture_templates.items():
            self.points = list(templatePoints)

            # print(self.points)
            
            self.resample()
            omega = self.indicative_angle()
            self.rotate_by(omega)
            # print(self.points)
            self.scale_to(self.SIZE)
            self.translate_to((0, 0))
            self.preprocessed_gesture_templates[templateName].append(self.points)
            # raw_gesture_templates["name of key"][0]["whatever coord you want"]

            

            # TODO: save preprocessed_gesture_templates to a file
            # with open("preprocessed_gestures.json", "w") as f:
            #     body = {templateName: self.points}
            #     json.dump(body, f)
    
    def path_length(self):  # Determines the total length of a given list of points.
        small_d = 0
        for i in range(1, len(self.points)):
            small_d += math.sqrt(
                math.pow((self.points[i][0]) - (self.points[i - 1][0]), 2)
                + math.pow((self.points[i][1]) - (self.points[i - 1][1]), 2)
            )
        return small_d

    def resample(self):  # Resamples the given list of points into N evenly spaced points.
        raw_list = self.points
        if len(raw_list) >= self.N_RESAMPLE_POINTS:
            resampled_list = [raw_list[0]]
            i = self.path_length() / (self.N_RESAMPLE_POINTS - 1)
            d = 0

            while len(raw_list) > 1:
                small_d = math.sqrt(
                    math.pow((raw_list[0][0]) - (raw_list[1][0]), 2)
                    + math.pow((raw_list[0][1]) - (raw_list[1][1]), 2)
                )

                if (d + small_d) >= i:
                    q_x = (raw_list[0][0]) + ((i - d) / small_d) * (
                        (raw_list[1][0]) - (raw_list[0][0])
                    )
                    q_y = (raw_list[0][1]) + ((i - d) / small_d) * (
                        (raw_list[1][1]) - (raw_list[0][1])
                    )
                    resampled_list.append((q_x, q_y))
                    raw_list.pop(0)
                    raw_list.insert(0, (q_x, q_y))
                    d = 0
                else:
                    raw_list.pop(0)
                    d += small_d

            if len(resampled_list) < self.N_RESAMPLE_POINTS:
                resampled_list.append(raw_list[0])

            return resampled_list

    def compute_centroid(self):
        centroid_x = sum(point[0] for point in self.points) / self.N_RESAMPLE_POINTS
        centroid_y = sum(point[1] for point in self.points) / self.N_RESAMPLE_POINTS

        return (centroid_x, centroid_y)

    def indicative_angle(self):
        centroid_x, centroid_y = self.compute_centroid()

        return math.atan2(
            centroid_y - self.points[0][1], centroid_x - self.points[0][0]
        )

    def rotate_by(self, omega):
        centroid_x, centroid_y = self.compute_centroid()
        rotated_points = []

        for point in self.points:
            q_x = point[0] - centroid_x
            q_y = point[1] - centroid_y
            rotated_x = q_x * math.cos(omega) - q_y * math.sin(omega) + centroid_x
            rotated_y = q_x * math.sin(omega) + q_y * math.cos(omega) + centroid_y
            rotated_points.append((rotated_x, rotated_y))

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

    def recognize(self, size: float | int) -> tuple:
        """
        identifies the gesture by comparing the given list of points to the stored gesture templates

        parameters:
        ----------
            size: the size passed to scale_to from step 3

        Returns:
        ----------
            a tuple containing (gesture, score)
        """
        b = float("inf")
        gesture = ""
        for t in self.raw_gesture_templates:
            d = self.distance_at_best_angle(self.raw_gesture_templates[t], -45, 45, 2)
            if d < b:
                b = d
                gesture = t
        score = 1 - (b / (0.5 * math.sqrt(size**2 + size**2)))
        return (gesture, score)

    def distance_at_best_angle(
        self, t: list, thetaA: float | int, thetaB: float | int, thetaDelta: float | int
    ) -> float:
        """
        finds the distance between the given list of points and the given gesture template at the best angle

        parameters:
        ----------
            t: the gesture template to compare the list of points to
            thetaA: the lower bound of the angle range to search in degrees
            thetaB: the upper bound of the angle range to search in degrees
            thetaDelta: the step size for the angle range in degrees

        Returns:
        ----------
            a float representing the distance at the best angle
        """
        phi = 0.5 * (-1 + math.sqrt(5))
        x1 = phi * thetaA + (1 - phi) * thetaB
        f1 = self.distance_at_angle(t, x1)
        x2 = (1 - phi) * thetaA + phi * thetaB
        f2 = self.distance_at_angle(t, x2)
        while abs(thetaB - thetaA) > thetaDelta:
            if f1 < f2:
                thetaB = x2
                x2 = x1
                f2 = f1
                x1 = phi * thetaA + (1 - phi) * thetaB
                f1 = self.distance_at_angle(t, x1)
            else:
                thetaA = x1
                x1 = x2
                f1 = f2
                x2 = (1 - phi) * thetaA + phi * thetaB
                f2 = self.distance_at_angle(t, x2)
        return min(f1, f2)

    def distance_at_angle(self, t: list, theta: float) -> float:
        """
        Finds the distance between the given list of points and the given gesture template at the given angle
        
        parameters:
        ----------
        t: the gesture template to compare the list of points to
        theta: the angle in degrees
        
        Returns:
        ----------
        The distance between the given list of points and the given gesture template at the given angle
        """
        newPts = self.rotate_by(theta)
        d = self.path_distance(newPts, t)
        return d

    def path_distance(self, a: list, b: list) -> float:
        """
        calculates the average distance between a and b point-wise

        parameters:
        ----------
        a: list of points for a in the format [(x, y), ...]
        b: list of points for b in the format [(x, y), ...]

        Returns:
        ----------
            the average distance between and b as a float
        """
        d = 0
        for i in range(min(len(a), len(b))):
            # calculate the distance between points a and b and add to d
            d += math.sqrt((a[i][0] - b[i][0]) ** 2 + (a[i][1] - b[i][1]) ** 2)
        return d / len(a)
    
    def run(self):
        self.resample()
        omega = self.indicative_angle()
        self.rotate_by(omega)
        self.scale_to(self.SIZE)
        self.translate_to((0, 0))
        self.recognize(self.SIZE)

if __name__ == "__main__":
    triangle_test = raw_gesture_templates["triangle"]
    triangle_recognizer = DollarRecognizer(triangle_test)
    print(triangle_recognizer.recognize(1))
