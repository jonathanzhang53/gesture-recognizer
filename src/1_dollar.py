from canvas import Canvas
from recognizer import DollarRecognizer
import stored_gestures

from collections import defaultdict
import random

live = False  # True = online mode, False = offline mode.

if __name__ == "__main__":
    if live:
        canvas = Canvas()
        canvas.run()
    else:
        gestures = [
            "triangle",
            "x",
            "rectangle",
            "circle",
            "check",
            "caret",
            "zig-zag",
            "arrow",
            "left square bracket",
            "right square bracket",
            "v",
            "delete",
            "left curly brace",
            "right curly brace",
            "star",
            "pigtail",
        ]

        print("Starting loop.")  # Loop over data set

        ### PSEUDOCODE
        # for each user U = 1 to 10
        #   for each example E = 1 to 9
        #       for i = 1 to 100
        #           for each gesture G in gestures
        #               choose E templates from U,G set
        #               choose 1 candidate from remaining templates
        #           for each candidate T from 1 to G
        #               recognize candidate with E chosen templates
        #               if recognition correct
        #                   increment recognition score for each U,G by 1
        #       recognition score for each U,G /= 100
        # print final average per-user accuracy
        # loop through each user, gathering recognition scores for 100 tests each involving 1 to 9 templates (900 tests x 16 gestures per user)
        for user in range(2, 12):
            for E in range(1, 10):
                # user recognition score for each example E
                user_recognition_score = 0
                user_recognition_scores = []
                for i in range(100):
                    recognizer = DollarRecognizer(
                        points=[], live=False
                    )  # Initialize recognizer in offline mode.
                    templates = defaultdict(list)
                    # key: gesture_name
                    # value: [template_1, template_2, ...]
                    candidates = defaultdict(list)
                    # key: gesture_name
                    # value: candidate_points

                    for gesture in gestures:
                        for j in range(1, E + 1):
                            # choose E templates from U,G set
                            possible_template = [i for i in range(10)]
                            this_template = possible_template.pop(
                                random.randint(0, len(possible_template) - 1)
                            )
                            #stored_gestures.preprocessed_datasetp[user][randomint]["gesture"]
                            templates[gesture].append(this_template)

                            # choose 1 candidate from remaining templates
                            this_candidate = possible_template.pop(
                                random.randint(0, len(possible_template) - 1)
                            )
                            candidates[gesture] = this_candidate
                    for candidate_name, candidate_points in candidates.items():
                        # TODO: process all templates stored in templates for each gesture
                        # recognize candidate with E chosen templates
                        recognizer.points = candidate_points
                        gesture_name, score = recognizer.run()

                        if gesture_name == candidate_name:
                            # increment recognition score for each user, gesture by 1
                            user_recognition_score += 1
                    # add recognition score for each user, gesture to user_recognition_scores
                    user_recognition_scores.append(user_recognition_score)
                # recognition score for each U,G /= 100
                user_recognition_scores = [
                    score / 100 for score in user_recognition_scores
                ]
        # print final average per-user accuracy
        for score in user_recognition_scores:
            print(score)
