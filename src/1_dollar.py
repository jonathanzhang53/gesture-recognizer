from canvas import Canvas
from recognizer import DollarRecognizer

live = False # True = online mode, False = offline mode.

if __name__ == "__main__":
    if live:
        canvas = Canvas()
        canvas.run()
    else:
        recognizer = DollarRecognizer([], False) # Initialize recognizer in offline mode.
    
        print("Starting loop.") # Loop over data set
        for user in range(2,12):
            for gesture_type in ["triangle","x","rectangle","circle","check","caret","zig-zag","arrow","left square bracket","right square bracket","v","delete","left curly brace","right curly brace","star","pigtail"]:
                for E in range(1,10):
                    for i in range(1,101):
                        #(work in progress)
                        blank_var_just_so_i_can_push = "delete me"
                        

