# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

from collections import defaultdict
import csv
import random
import time
import sys
import os
from pathlib import Path

from canvas import Canvas
from recognizer import DollarRecognizer
import stored_gestures


def str2bool(v: str) -> bool:
    return v.lower() in ("yes", "true", "t", "1")


# python3 1_dollar.py [live: boolean ("yes", "true", "t", "1")] [offline_i: int] [num_users: int] [dataset: string ("xml_logs", "user_gestures")]
try:
    live = str2bool(sys.argv[1])
    if not live:
        # OFFLINE_I: number of offline tests to run per user and E-level (set to 1 for demo, 10 for fast, 100 for accurate)
        # NUM_USERS: number of users to test
        # DATASET: which dataset to use. (use "xml_logs" or "user_gestures")
        try:
            OFFLINE_I = int(sys.argv[2])
        except:
            print("No command line argument found for OFFLINE_I: defaulting to I = 10.")
            OFFLINE_I = 10

        try:
            NUM_USERS = int(sys.argv[3])
        except:
            print("No command line argument found for NUM_USERS: defaulting to 1 user.")
            NUM_USERS = 1

        try:
            DATASET = str(sys.argv[4])
        except:
            print("No command line argument found for DATASET: defaulting to \"xml_logs\".")
            DATASET = "xml_logs"
except:
    print("No command line argument found: defaulting to offline mode.")
    live = False  # True = online mode, False = offline mode.


if __name__ == "__main__":
    if live:
        canvas = Canvas([False])
        canvas.run()
    else:
        if DATASET == "xml_logs":
            gestures = [
            "triangle",
            "x",
            "rectangle",
            "circle",
            "check",
            "caret",
            "question_mark",
            "arrow",
            "left_sq_bracket",
            "right_sq_bracket",
            "v",
            "delete_mark",
            "left_curly_brace",
            "right_curly_brace",
            "star",
            "pigtail",
        ]
        elif DATASET == "user_gestures":
            gestures = [
            "arrow",
            "caret",
            "check",
            "circle",
            "delete",
            "left_curly_brace",
            "left_square_bracket",
            "pigtail",
            "rectangle",
            "right_curly_brace",
            "right_square_bracket",
            "star",
            "triangle",
            "v",
            "x",
            "zig-zag",
        ]

        print("Starting loop.")  # loop over data set

        path = Path(os.getcwd())
        path = path.parent.absolute()
        path = str(path) + "\\recognition_logs\\recognition_log.csv"
        file = open(
            path, "w", newline="", encoding="UTF-8"
        )  # open csv file for logging results
        log = csv.writer(file)
        log.writerow(
            [
                "Recognition Log: Katherine Chan, Thomas Ruby, Jonathan Zhang // $1 Recognizer // XML Dataset // USER-DEPENDENT RANDOM-"
                + str(OFFLINE_I)
            ]
        )
        log.writerow(
            [
                "User[all-users]",
                "GestureType[all-gesture-types]",
                "Random Iteration[1to" + str(OFFLINE_I) + "]",
                "#ofTrainingExamples[E]",
                "TotalSizeOfTrainingSet[count]",
                "TrainingSetContents[specific-gesture-instances]",
                "Candidate[specific-instance]",
                "RecoResultGestureType[what-was-recognized]",
                "CorrectIncorrect[1or0]",
                "RecoResultScore",
                "RecoResultBestMatch[specific-instance]",
                "RecoResultNBestSorted[instance-and-score]",
            ]
        )

        print("Beginning random loop with I = " + str(OFFLINE_I))

        recognizer = DollarRecognizer(
            points=[], live=False, dataset=DATASET
        )  # initialize recognizer in offline mode


        time_last = 0
        user_accuracies = []  # average recognition percentages for each user
        user_range = range(2, 2  + NUM_USERS)
        if DATASET == "user_gestures":
            user_range = range(1, 1 + NUM_USERS)

        for user in user_range:
            time_current = time.time()
            user_recognition_scores = []  # user recognition score for each example E

            print("\tUser " + str(user))

            if time_last != 0:
                print(
                    "\tEstimated time remaining: "
                    + str(int((time_current - time_last) * (user_range.stop - user) / 60))
                    + " minutes "
                    + str(int((time_current - time_last) * (user_range.stop - user) % 60))
                    + " seconds."
                )

            for E in range(1,10):
                print("\t\tE = " + str(E))

                user_recognition_score = 0
                for i in range(OFFLINE_I):
                    templates = defaultdict(list)
                    # key: gesture_name
                    # value: [template_1, template_2, ...]
                    candidates = defaultdict(list)
                    # key: gesture_name
                    # value: candidate_points

                    for gesture in gestures:
                        possible_template = [i for i in range(1, 11)]

                        for j in range(1, E + 1):
                            # choose E templates from U,G set
                            this_template = possible_template.pop(
                                random.randint(0, len(possible_template) - 1)
                            )
                            if (
                                this_template < 10
                            ):  # If user is single digit, add a 0 to the front of the string. So, a triangle is saved as "triangle01", and etc.
                                templates[gesture + "0" + str(this_template)].append(
                                    stored_gestures.preprocessed_dataset[user][
                                        gesture + "0" + str(this_template)
                                    ]
                                )
                            else:
                                templates[gesture + str(this_template)].append(
                                    stored_gestures.preprocessed_dataset[user][
                                        gesture + str(this_template)
                                    ]
                                )

                        # choose 1 candidate from remaining templates
                        this_candidate = possible_template.pop(
                            random.randint(0, len(possible_template) - 1)
                        )
                        if this_candidate < 10:
                            # if this_candidate is single digit, add a 0 to the front of the string. So, a triangle is saved as "triangle01", and etc.
                            candidates[gesture + "0" + str(this_candidate)].append(
                                stored_gestures.preprocessed_dataset[user][
                                    gesture + "0" + str(this_candidate)
                                ]
                            )
                            '''print("----------")
                            print(user)
                            print(gesture + "0" + str(this_candidate))
                            print(stored_gestures.preprocessed_dataset[user][
                                    gesture + "0" + str(this_candidate)
                                ])'''
                        else:
                            candidates[gesture + str(this_candidate)].append(
                                stored_gestures.preprocessed_dataset[user][
                                    gesture + str(this_candidate)
                                ]
                            )
                            '''print("----------")
                            print(user)
                            print(gesture + str(this_candidate))
                            print(stored_gestures.preprocessed_dataset[user][
                                    gesture + str(this_candidate)
                                ])'''

                    recognizer.clearTrainingSet()
                    #print("\t\t\tTraining set: " + str(templates))
                    #print(stored_gestures.preprocessed_dataset[1].keys())
                    #print(stored_gestures.preprocessed_dataset[1]["arrow03"])
                    recognizer.setOfflineTrainingSet(templates)

                    for candidate_name, candidate_points in candidates.items():
                        # recognize candidate with E chosen templates
                        recognizer.points = candidate_points[
                            0
                        ]  # so we only want the first list
                        gesture_name, score, N_best_list = recognizer.recognize(
                            recognizer.SIZE
                        )

                        if score > 0.9999:  # Score should never be exactly 1
                            print(
                                "WARNING! Recognizer returned a score very nearly == 1. Is a gesture in both the training and testing sets?"
                            )

                        reco_result = int(gesture_name[:-2] == candidate_name[:-2])
                        user_recognition_score += reco_result

                        if reco_result == 0:
                            print(
                                "\t\t\t\t--Incorrectly recognized "
                                + candidate_name
                                + " as "
                                + gesture_name
                                + "."
                            )

                        template_keys = (
                            "{"
                            + str(templates.keys())[11 : len(str(templates.keys())) - 2]
                            + "}"
                        )

                        # add to log
                        log.writerow(
                            [
                                user,
                                candidate_name[:-2],
                                i + 1,
                                E,
                                len(templates),
                                template_keys,
                                candidate_name,
                                gesture_name[:-2],
                                reco_result,
                                score,
                                gesture_name,
                                N_best_list[:50],
                            ]
                        )

                print(
                    "\t\t\t\t"
                    + str(user_recognition_score)
                    + " of "
                    + str(OFFLINE_I * 16)
                    + " gestures ("
                    + (str(100 * (user_recognition_score / (OFFLINE_I * 16)))[:5])
                    + "%) recognized correctly for E = "
                    + str(E)
                    + "."
                )

                # add the recognition score for this E of this user
                user_recognition_scores.append(user_recognition_score)

            # recognition score for each U,G /= 100
            user_recognition_scores = [
                score / OFFLINE_I for score in user_recognition_scores
            ]
            log.writerow("")
            log.writerow(
                [
                    "TotalAvgAccuracy[User=" + str(user) + "]",
                    (sum(user_recognition_scores) / len(user_recognition_scores))
                    / len(gestures),
                ]
            )
            log.writerow("")
            log.writerow("")
            user_accuracies.append(
                (sum(user_recognition_scores) / len(user_recognition_scores))
                / len(gestures)
            )
            time_last = time_current  # for estimated time remaining

        log.writerow(
            [
                "TotalAvgAccuracy[AllUsers]",
                (sum(user_accuracies) / len(user_accuracies)),
            ]
        )
        log.writerow("")
        file.close()

        print("See recognition_log.csv for results.")
