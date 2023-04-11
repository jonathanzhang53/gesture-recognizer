# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

from recognizer import DollarRecognizer

import tkinter as tk


class Canvas:
    """
    Canvas class for drawing gestures
    """

    N_RESAMPLE_POINTS = 64

    def __init__(self):
        # location of last drawn point
        self.last_x = None
        self.last_y = None

        # contains the raw points for the user's currently drawn gesture
        self.raw_input_points = []

        # GUI setup
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=300, height=200)
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

        # CANVAS
        self.canvas.config(bg="gray")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouseup_recognize)

        # CLEAR BUTTON
        clear_button = tk.Button(
            self.root, text="Clear Canvas", command=self.clear_canvas
        )
        clear_button.pack()

        # MAIN LOOP
        self.root.mainloop()

    def on_mouseup_recognize(self, event):
        """
        When the mouse is released (in ONLINE mode), run the recognizer and display the result.
        """
        self.last_x = None
        self.last_y = None
        self.dollar_recognizer.points = self.raw_input_points
        name_of_gesture, gesture_score, N_best_list = self.dollar_recognizer.run()
        self.text.delete("1.0", "end")
        self.text.insert(
            "1.0",
            "Result: " + name_of_gesture + ", Score: " + str(gesture_score)[0:5],
        )

    def paint(self, event):
        """
        Draw on the canvas with the mouse
        MouseDown (start of input), MouseDragged (input continues), and MouseUp (input ends)
        """
        if (self.last_x, self.last_y) != (None, None):
            self.canvas.create_line(
                (self.last_x, self.last_y), (event.x, event.y), width=2
            )
        else:
            self.clear_canvas()

        self.last_x = event.x
        self.last_y = event.y
        self.raw_input_points.append((event.x, event.y))

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
