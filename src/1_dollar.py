from canvas import Canvas
from recognizer import DollarRecognizer
import stored_gestures
import csv
from collections import defaultdict
import random
import time

live = False  # True = online mode, False = offline mode.
OFFLINE_I = 10 # number of offline tests to run per user and E-level. (set to 10 for fast, 100 for accurate)

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
        file = open("Recognition Log.csv", "w", newline="")
        log = csv.writer(file) 
        log.writerow(["Recognition Log: Katherine Chan, Thomas Ruby, Jonathan Zhang // $1 Recognizer // XML Dataset // USER-DEPENDENT RANDOM-"+str(OFFLINE_I)])
        log.writerow(["User", "Gesture Type", "Random Iteration[1 to "+str(OFFLINE_I)+"]", "#ofTrainingExamples[E]", "TotalSizeOfTrainingSet", "TrainingSetContents","Candidate","RecoResultGestureType[what-was-recognized]","CorrectIncorrect[1or0]","RecoResultScore", "RecoResultBestMatch[specific-instance]","RecoResultNBestSorted[instance-and-score]"])
        
        print("Begining random-100 loop with I = " + str(OFFLINE_I))
        recognizer = DollarRecognizer(
                        points=[], live=False
                    )  # Initialize recognizer in offline mode.
        time_last = 0 # for estimated time remaining
        for user in range(2, 12):
            time_current = time.time() # for estimated time remaining
            user_recognition_scores = [] # user recognition score for each example E
            print("\tUser " + str(user) + " of 11.")
            if time_last != 0: # print estimated time remaining
                print("\tEstimated time remaining: " + str(int((time_current - time_last) * (11 - user)/60)) + " minutes " + str(int((time_current - time_last) * (11 - user)%60)) + " seconds.")
            for E in range(1, 10):
                print("\t\tE = " + str(E) + " of 9.  ", end="\n")
                user_recognition_score = 0
                for i in range(OFFLINE_I):
                    templates = defaultdict(list)
                    # key: gesture_name
                    # value: [template_1, template_2, ...]
                    candidates = defaultdict(list)
                    # key: gesture_name
                    # value: candidate_points

                    for gesture in gestures:
                        possible_template = [i for i in range(1,11)]
                        for j in range(1, E + 1):
                            # choose E templates from U,G set
                            this_template = possible_template.pop(
                                random.randint(0, len(possible_template) - 1)
                            )
                            if this_template < 10: # If user is single digit, add a 0 to the front of the string. So, a triangle is saved as "triangle01", and etc.
                                templates[gesture + "0" + str(this_template)].append(stored_gestures.preprocessed_dataset[user][gesture+ "0" +str(this_template)])
                            else:
                                templates[gesture + str(this_template)].append(stored_gestures.preprocessed_dataset[user][gesture+str(this_template)])

                        # choose 1 candidate from remaining templates
                        this_candidate = possible_template.pop(
                            random.randint(0, len(possible_template) - 1)
                        )
                        if this_candidate < 10: # If this_candidate is single digit, add a 0 to the front of the string. So, a triangle is saved as "triangle01", and etc.
                            candidates[gesture + "0" + str(this_candidate)].append(stored_gestures.preprocessed_dataset[user][gesture+ "0" +str(this_candidate)])
                        else:
                            candidates[gesture + str(this_candidate)].append(stored_gestures.preprocessed_dataset[user][gesture+str(this_candidate)])
                    
                    recognizer.clearTrainingSet()
                    recognizer.setOfflineTrainingSet(templates)
                    for candidate_name, candidate_points in candidates.items():
                        # recognize candidate with E chosen templates
                        recognizer.points = candidate_points[0] #(is double nested list, so we only want the first list)
                        gesture_name, score, N_best_list = recognizer.recognize(recognizer.SIZE)
                        if score > 0.9999: # Score should never be exactly 1
                            print("WARNING! Recognizer returned a score very nearly == 1. Is a gesture in both the training and testing sets?")
                        
                        if gesture_name[:-2] == candidate_name[:-2]:
                            user_recognition_score += 1 # increment recognition score for each user, gesture by 1
                            #Add to log
                            log.writerow([user, candidate_name[:-2], i+1, E, len(templates), templates.keys(), candidate_name, gesture_name[:-2], 1, score, gesture_name, N_best_list[:50]])
                        else:
                            print("\t\t\t\t--Incorrectly recognized " + candidate_name + " as " + gesture_name + ".")
                            #Add to log
                            log.writerow([user, candidate_name[:-2], i+1, E, len(templates), templates.keys(), candidate_name, gesture_name[:-2], 0, score, gesture_name, N_best_list[:50]])
                
                print("\t\t\t\t"+str(user_recognition_score)+ " of " + str(OFFLINE_I*16) +  " gestures (" + (str(100*(user_recognition_score/(OFFLINE_I*16)))[:5]) + "%) recognized correctly for E = " + str(E) + ".")
                # add the recognition score for this E of this user
                user_recognition_scores.append(user_recognition_score)
                # recognition score for each U,G /= 100

            user_recognition_scores = [
                score / OFFLINE_I for score in user_recognition_scores
            ]
            log.writerow("")
            log.writerow(["TotalAvgAccuracy[User=" + str(user) + "]",(sum(user_recognition_scores)/len(user_recognition_scores))/len(gestures)])
            log.writerow("")
            log.writerow("")
            time_last = time_current # for estimated time remaining
        
        file.close()    
        print("Random 100 loop complete. See Recognition Log.csv for results.")   
