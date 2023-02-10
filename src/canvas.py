# Python GUI library
import tkinter as tk

from recognizer import DollarRecognizer

class Canvas:
    """Canvas class for drawing gestures"""

    N_RESAMPLE_POINTS = 64

    def __init__(self):
        # location of last drawn point
        self.last_x = None
        self.last_y = None

        # contains the raw points for the user's currently drawn gesture
        self.raw_input_points = []

        # GUI setup
        self.root = tk.Tk()
        self.text = tk.Text(self.root, height=1, width=40)
        self.canvas = tk.Canvas(self.root, width=300, height=200)

        # initialize DollarRecognizer
        self.dollar_recognizer = DollarRecognizer(self.raw_input_points)

    def run(self):
        """Run the canvas."""
        # ROOT WINDOW
        self.root.title("My Canvas")

        # TEXT
        self.text.pack()

        # CANVAS
        self.canvas.config(bg="gray")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouseup)

        # CLEAR BUTTON
        clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack()

        # MAIN LOOP
        self.root.mainloop()

    def on_mouseup(self, event):
        self.last_x = None
        self.last_y = None
        self.dollar_recognizer.points = self.raw_input_points
        self.dollar_recognizer.run()

    def paint(self, event):
        """ 
        Draw on the canvas with the mouse.
        MouseDown (start of input), MouseDragged (input continues), and MouseUp (input ends).
        """
        if (self.last_x, self.last_y) != (None, None):
            self.canvas.create_line((self.last_x, self.last_y), (event.x, event.y), width=2)
        else:
            self.clear_canvas()
        
        self.last_x = event.x
        self.last_y = event.y
        self.raw_input_points.append((event.x, event.y))
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "N = " + str(len(self.raw_input_points)))

    def clear_canvas(self):
        """
        Clear the canvas and reset the stroke points.
        """
        self.canvas.delete("all")
        self.raw_input_points.clear()
        self.last_x = None
        self.last_y = None
