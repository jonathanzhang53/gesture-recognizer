# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

from collections import defaultdict
import tkinter as tk
from tkinter import PhotoImage
from bs4 import BeautifulSoup
from recognizer import DollarRecognizer
import os
from pathlib import Path
from datetime import datetime

class Canvas:
    """
    Canvas class for drawing gestures
    """

    N_RESAMPLE_POINTS = 64

    def __init__(self, cmd_args):
        self.gather_mode = False
        if cmd_args.__len__() == 2:
            self.gather_mode = bool(cmd_args[1])
            self.username = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # use the current time to generate a new username
            self.sample_count = 1
        elif cmd_args.__len__() == 3:
            self.gather_mode = bool(cmd_args[1])
            self.username = str(cmd_args[2])
            self.sample_count = 1
        elif cmd_args.__len__() == 4:
            self.gather_mode = bool(cmd_args[1])
            self.username = str(cmd_args[2])
            self.sample_count = int(cmd_args[3])

        # location of last drawn point
        self.last_x = None
        self.last_y = None

        # contains the raw points for the user's currently drawn gesture
        self.raw_input_points = []

        if self.gather_mode:
            self.all_gesture_names = ["triangle", "x", "rectangle", "circle", "check", "caret", "zig-zag", "arrow", "left_square_bracket", "right_square_bracket", "v", "delete", "left_curly_brace", "right_curly_brace", "star", "pigtail"]

        # GUI setup
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=300, height=200)
        if self.gather_mode:
            self.text = tk.Text(self.root, height=1, width=40, background="light grey", font=("Courier", 11))
            self.text2 = tk.Text(self.root, height=2, width=36, background="light grey", font=("Courier", 13, "bold"))
            self.gathered_gestures = defaultdict(list)
            self.current_gesture_name = self.all_gesture_names[(self.sample_count-1)%self.all_gesture_names.__len__()]
        else:
            self.text = tk.Text(self.root, height=1, width=40)

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
            self.text2.pack()
            self.text.insert("1.0", "Sample " + str(self.sample_count) + " of 160")
            self.text2.insert("1.0", "Please draw a: " + str.upper(self.current_gesture_name))

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

        # REFERENCE IMAGE FOR GATHER_MODE
        if self.gather_mode:
            path = Path(os.getcwd())
            path = path.parent.absolute()
            path = str(path) + "\\unistrokes_smaller.png"
            img = PhotoImage(file=path)
            tk.Label(self.root, image=img).pack()

        # MAIN LOOP
        self.root.mainloop()

    def on_mouseup_recognize(self, event):
        """
        When the mouse is released (in ONLINE mode), run the recognizer and display the result.
        """
        self.last_x = None
        self.last_y = None
        if not self.gather_mode:
            self.dollar_recognizer.points = self.raw_input_points
            name_of_gesture, gesture_score, N_best_list = (self.dollar_recognizer.run())
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "Result: " + name_of_gesture + ", Score: " + str(gesture_score)[0:5])

    def store_gesture(self):
        """
        Store the gesture in XML format
        """
        if self.sample_count > 160: # Do not continue if already gathered 160 gestures.
            return
        
        # append raw points to gesture list
        self.gathered_gestures[self.current_gesture_name].append(self.raw_input_points)

        # write raw points to XML file
        self.recordXMLfile()

        # increment sample count
        self.sample_count += 1

        # update current gesture name
        # TODO: make this random (?)
        self.current_gesture_name = self.all_gesture_names[(self.sample_count-1)%self.all_gesture_names.__len__()]

        # update text
        self.text.delete("1.0", "end")
        self.text2.delete("1.0", "end")
        self.text.insert("1.0", "Sample " + str(self.sample_count) + " of 160")
        self.text2.insert("1.0", "Please draw a: " + str.upper(self.current_gesture_name))

        # clear canvas for next sample
        self.clear_canvas()

        #If gathered 160 samples, display so to user
        if self.sample_count > 160:
            self.text.delete("1.0", "end")
            self.text2.delete("1.0", "end")
            self.text2.insert("1.0", "All done! Thank you for your time.")
    
    def recordXMLfile(self):
        """
        Record the gestures in XML format
        """
        # create XML file
        path = Path(os.getcwd())
        path = path.parent.absolute()
        path = str(path) + "\\user_gestures\\" + str(self.username)
        if not os.path.exists(path):
            os.makedirs(path)
        xml_file = open(str(path) + "\\" + str(self.current_gesture_name) + str(int((self.sample_count-1)/16)) + ".xml", "w")
        xml_file.write("<Gesture Name = " + str(self.current_gesture_name) + str(int((self.sample_count-1)/16)) + ">\n")

        # write each point to XML file
        for point in self.raw_input_points:
            xml_file.write("\t<Point X=\"" + str(point[0]) + "\" Y=\"" + str(point[1]) + "\"/>\n")

        # close XML file
        xml_file.write("</Gesture>")
        xml_file.close()

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
