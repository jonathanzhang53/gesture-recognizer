from canvas import Canvas
from recognizer import DollarRecognizer
from collections import defaultdict
import random
import stored_gestures

live = False # True = online mode, False = offline mode.
if __name__ == "__main__":
    if live:
        canvas = Canvas()
        canvas.run()
    else:
        recognizer = DollarRecognizer([], False) # Initialize recognizer in offline mode.
    
        print("Starting loop.") # Loop over data set
        gestures = ["triangle", "x", "rectangle", "circle", "check", "caret", "zig-zag", "arrow", "left square bracket", "right square bracket", "v", "delete", "left curly brace", "right curly brace", "star", "pigtail"]
        for user in range(2, 12):
            for E in range(1, 10):
                for i in range(100):
                    candidates = defaultdict(list)

                    # key: gesture_name
                        # value: [[points for template_1], [points for template_2]]
                    training_set = map()
                    for gesture in gestures:              
                        # choose E templates
                        possible_instances = [i for i in range(10)]
                        for j in range(1,E+1): 
                            for gesture_2 in gestures:
                                # pick a random instance and take it out of the list
                                this_instance = possible_instances.pop(random.randint(0, len(possible_instances)-1))
                                training_set[f"{gesture}{E}"] = stored_gestures.preprocessed_dataset[user][this_instance][gesture_2]
                            
                        this_instance = possible_instances.pop(random.randint(0, len(possible_instances)-1))
                        candidate = stored_gestures.preprocessed_dataset[user][this_instance][gesture]
                        # choose 1 candidate from remaining templates
                        # candidates["template_name"] = template_points
                    for candidate_name, candidate_points in candidates.items():
                        # recognize candidate with E chosen templates
                        #TODO: insert points
                        recognizer.points = candidate_points
                        print(recognizer.run())             
                        

