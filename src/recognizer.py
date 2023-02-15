# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

import math, os
from collections import defaultdict
import stored_gestures
from bs4 import BeautifulSoup

class DollarRecognizer:
    N_RESAMPLE_POINTS = 64
    SIZE = 250

    def __init__(self, points, live=True) -> None:
        """
        Initializes the DollarRecognizer class by setting class variables and calling the processTemplates method
        
        parameters:
        ----------
            points: list of points in the format [(x, y), ...]
            live: indicates whether online/offline. If offline, read and process XML data.
        """
        if not live:
            self.raw_gesture_templates = stored_gestures.default_raw_gesture_templates
            self.preprocessed_gesture_templates = defaultdict(dict)
            self.readXMLDataset()
        self.raw_gesture_templates = stored_gestures.default_raw_gesture_templates
        self.preprocessed_gesture_templates = defaultdict(list) # hashmap of with key = gesture name and value = list of templates
        self.points = points
        self.processTemplates()

    def readXMLDataset(self,speed="medium") -> None:
        """
        Populates stored_gestures.preprocessed_dataset with the data that is contained in the xml_logs
        
        parameters:
        ----------
            speed: specifies which speed type of data is to be read. Use "slow", "medium", or "fast".
        """
        self.preprocessed_gesture_templates.clear()
        print("Reading and processing xml_logs. This may take a minute.")
        for s in range(2,12):
            dataset_subset = {}
            if s >= 10:
                s = str(s)
            elif s < 10:
                s = "0" + str(s)
            print("\tProcessing user " + s + " of 11")
            path = os.getcwd() + "\\xml_logs\\s" + s + "\\" + speed
            list_of_files = os.listdir(path)
            for i in range(1,11):
                if i >= 10:
                    i = str(i)
                elif i < 10:
                    i = "0" + str(i)
                self.preprocessed_gesture_templates.clear()
                file_set = []
                for file_name in list_of_files:
                    if file_name.find(s) != -1:
                        file_set.append(file_name)
                for file_name in file_set:
                    self.points = ()
                    file = open(path+"\\"+file_name, 'r')
                    file_XML_data = BeautifulSoup(file.read(),'lxml')
                    all_points_XML = file_XML_data.find_all('point')
                    for point_XML in all_points_XML:
                        self.points += (int(point_XML["x"]),int(point_XML["y"]))
                self.processTemplates(read=True)
                dataset_subset[int(i)] = self.preprocessed_gesture_templates
            stored_gestures.preprocessed_dataset[int(s)] = dataset_subset
        print("Done reading xml_logs.")
        # Uncomment the below lines to inspect the contents of stored_gestures.preprocessed_dataset
        """text_file = open("processed_data.txt","w")
        text_file.write(str(stored_gestures.preprocessed_dataset))
        text_file.close()"""
    
    def setTrainingSet(self, training_set) -> None:
        """
        Adds the list of points to the recognizer's training set.

        parameters:
        ----------
            training_set: map of training set of type {gesture : [points]}
        """
        for gesture, points in training_set:
            self.preprocessed_gesture_templates[gesture] = points

    def clearTrainingSet(self) -> None:
        """
        Clears the recognizer's training set.

        parameters:
        ----------
            points: preprocessed list of points to add.
        """
        self.preprocessed_gesture_templates.clear()

    def processTemplates(self, read=False) -> None:
        """
        Preprocesses the raw gesture templates and saves them to a file

        parameters:
        ----------
            read: if reading xml_logs, add points to defaultdict(dict) structure instead of defaultdict(list).
        """
        for templateName, templatePoints in self.raw_gesture_templates.items():
            self.points = list(templatePoints)
            self.points = self.resample()
            omega = self.indicative_angle()
            self.points = self.rotate_by(omega)
            self.points = self.scale_to(self.SIZE)
            self.points = self.translate_to((0, 0))
            if read:
                self.preprocessed_gesture_templates[templateName] = self.points
            else:
                self.preprocessed_gesture_templates[templateName].append(self.points)

            # TODO: save preprocessed_gesture_templates to a file
            # with open("preprocessed_gestures.json", "w") as f:
            #     body = {templateName: self.points}
            #     json.dump(body, f)
    
    def path_length(self) -> float:
        """
        Determines the total length of a given list of points

        Returns:
        ----------
            the total length of a given list of points
        """
        small_d = 0

        for i in range(1, len(self.points)):
            small_d += math.sqrt(
                math.pow((self.points[i][0]) - (self.points[i - 1][0]), 2)
                + math.pow((self.points[i][1]) - (self.points[i - 1][1]), 2)
            )

        return small_d

    def resample(self) -> list:
        """
        Resamples the given list of points into N evenly spaced points.

        Returns:
        ----------
            a resampled list of points of length N in the format [(x, y), ...]
        """
        raw_list = self.points
        if len(raw_list) > 0:
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

    def compute_centroid(self) -> tuple:
        """
        Computes the centroid of all points
        
        Returns:
        ----------
            the centroid as a tuple in the format (x, y)
        """
        centroid_x = sum(point[0] for point in self.points) / self.N_RESAMPLE_POINTS
        centroid_y = sum(point[1] for point in self.points) / self.N_RESAMPLE_POINTS

        return (centroid_x, centroid_y)

    def indicative_angle(self) -> float:
        """
        Finds the indicative angle based on the centroid and the first point
        
        Returns:
        ----------
            the indicative angle as a float in degrees
        """
        centroid_x, centroid_y = self.compute_centroid()

        return math.atan2(
            centroid_y - self.points[0][1], centroid_x - self.points[0][0]
        )

    def rotate_by(self, omega) -> list:
        """
        Rotates all points by the indicative angle
        
        parameters:
        ----------
            omega: indicative angle in degrees
        
        Returns:
        ----------
            a list of points rotated by the indicative angle in the format [(x, y), ...)]
        """
        centroid_x, centroid_y = self.compute_centroid()
        rotated_points = []

        for point in self.points:
            q_x = point[0] - centroid_x
            q_y = point[1] - centroid_y
            rotated_x = q_x * math.cos(omega) - q_y * math.sin(omega) + centroid_x
            rotated_y = q_x * math.sin(omega) + q_y * math.cos(omega) + centroid_y
            rotated_points.append((rotated_x, rotated_y))

        return rotated_points

    def scale_to(self, size) -> list:
        """
        Scales all points to a given size
        
        parameters:
        ----------
            size: predetermined size value to scale to
        
        Returns:
        ----------
            a list of points scaled to the predetermined size in the format [(x, y), ...)]
        """
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

    def translate_to(self, k) -> list:
        """
        Translates the points to a center.

        parameters:
        ----------
            k: origin to translate the points to.

        Returns:
        ----------
            a list of translated points in the format [(x, y), ...)]
        """
        centroid_x, centroid_y = self.compute_centroid()

        translated_points = []

        for point in self.points:
            q_x = point[0] + k[0] - centroid_x
            q_y = point[1] + k[1] - centroid_y
            translated_points.append((q_x, q_y))

        return translated_points

    def recognize(self, size: float | int) -> tuple:
        """
        Identifies the gesture by comparing the given list of points to the stored gesture templates

        parameters:
        ----------
            size: the size passed to scale_to from step 3

        Returns:
        ----------
            a tuple containing (gesture, score)
        """
        b = float("inf")
        gesture = ""

        for tName, tPoints in self.preprocessed_gesture_templates.items():
            d = self.distance_at_best_angle(tPoints[0], -45, 45, 2)
            if d < b:
                b = d
                gesture = tName
        score = 1 - (b / (0.5 * math.sqrt(size**2 + size**2)))
        print(gesture)
        return (gesture, score)

    def distance_at_best_angle(
        self, t: list, thetaA: float | int, thetaB: float | int, thetaDelta: float | int
    ) -> float:
        """
        Finds the distance between the given list of points and the given gesture template at the best angle

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
            the distance between the given list of points and the given gesture template at the given angle
        """
        newPts = self.rotate_by(theta)
        d = self.path_distance(newPts, t)

        return d

    def path_distance(self, a: list, b: list) -> float:
        """
        Calculates the average distance between a and b point-wise

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
    
    def run(self) -> tuple:
        self.points = self.resample()
        omega = self.indicative_angle()
        self.points = self.rotate_by(omega)
        self.points = self.scale_to(self.SIZE)
        self.points = self.translate_to((0, 0))
        gesture, score = self.recognize(self.SIZE)

        return (gesture, score)

if __name__ == "__main__":
    triangle_test = stored_gestures.default_raw_gesture_templates["triangle"]
    triangle_recognizer = DollarRecognizer(triangle_test)
    print(triangle_recognizer.recognize(250))
