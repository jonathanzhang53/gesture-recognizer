# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

from collections import defaultdict
import tkinter as tk

from recognizer import DollarRecognizer

class Canvas:
    """
    Canvas class for drawing gestures
    """

    N_RESAMPLE_POINTS = 64

    def __init__(self, gather_mode=False):
        # location of last drawn point
        self.last_x = None
        self.last_y = None

        # contains the raw points for the user's currently drawn gesture
        self.raw_input_points = []

        # GUI setup
        self.root = tk.Tk()
        self.text = tk.Text(self.root, height=1, width=40)
        self.canvas = tk.Canvas(self.root, width=300, height=200)
        self.gather_mode = gather_mode
        if self.gather_mode:
            self.gathered_gestures = defaultdict(list)
            self.sample_count = 1
            self.current_gesture_name = ""

        # initialize DollarRecognizer
        self.dollar_recognizer = DollarRecognizer(self.raw_input_points, True)

    def run(self):
        """
        Run the canvas
        """
        # ROOT WINDOW
        self.root.title("My Canvas")

        # TEXT
        self.text.pack()
        if self.gather_mode:
            self.text.insert("1.0", "Sample " + str(self.sample_count) + " of 160")

        # CANVAS
        self.canvas.config(bg="gray")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouseup_recognize)

        # CLEAR BUTTON
        clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack()

        # NEXT BUTTON FOR GATHER_MODE
        if self.gather_mode:
            next_button = tk.Button(self.root, text="Next Sample", command=self.store_gesture)
            next_button.pack()

        # MAIN LOOP
        self.root.mainloop()

    def on_mouseup_recognize(self, event):
        """
        When the mouse is released, run the recognizer and display the result
        """
        self.last_x = None
        self.last_y = None
        self.dollar_recognizer.points = self.raw_input_points
        if not self.gather_mode:
            name_of_gesture, gesture_score, N_best_list = (self.dollar_recognizer.run())
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "Result: " + name_of_gesture + ", Score: " + str(gesture_score)[0:5])

    def store_gesture(self):
        """
        Store the gesture in XML format
        """
        # append raw points to gesture list
        self.gathered_gestures[self.current_gesture_name].append(self.raw_input_points)

        # increment sample count
        self.sample_count += 1
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "Sample " + str(self.sample_count) + " of 160")

        # TODO: save to XML file
        print(self.raw_input_points)

        # clear canvas for next sample
        self.clear_canvas()

    def paint(self, event):
        """ 
        Draw on the canvas with the mouse
        MouseDown (start of input), MouseDragged (input continues), and MouseUp (input ends)
        """
        if (self.last_x, self.last_y) != (None, None):
            self.canvas.create_line((self.last_x, self.last_y), (event.x, event.y), width=2)
        else:
            self.clear_canvas()
        
        self.last_x = event.x
        self.last_y = event.y
        self.raw_input_points.append((event.x, event.y))

        if not self.gather_mode:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "N = " + str(len(self.raw_input_points)))

    def clear_canvas(self):
        """
        Clear the canvas and reset the stroke points
        """
        self.canvas.delete("all")
        self.raw_input_points.clear()
        self.last_x = None
        self.last_y = None
