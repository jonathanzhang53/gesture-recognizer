# Python GUI library
import tkinter as tk
import math

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

        # CLEAR BUTTON
        clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack()

        # DEBUG: RESAMPLE BUTTON
        debug_resample_button = tk.Button(self.root, text="DEBUG: resample", command=self.resample)
        debug_resample_button.pack()

        # MAIN LOOP
        self.root.mainloop()

    def path_length(self, A):
        """
        Determines the total length of a given list of points.
        """
        small_d = 0
        for i in range(1, len(A)):
            small_d += (math.sqrt(math.pow((A[i][0]) - (A[i-1][0]), 2)+math.pow((A[i][1]) - (A[i-1][1]), 2)))
        return small_d

    def resample(self):
        """
        Resamples the given list of points into N evenly spaced points.
        """
        raw_list = self.raw_input_points
        if len(raw_list) < self.N_RESAMPLE_POINTS:
            self.text.insert("4.0", ", Not enough points to resample!")
        else:
            resampled_list = [raw_list[0]]
            i = self.path_length(raw_list) / (self.N_RESAMPLE_POINTS - 1)
            d = 0

            while len(raw_list) > 1:
                small_d = math.sqrt(math.pow((raw_list[0][0]) - (raw_list[1][0]), 2) + math.pow((raw_list[0][1]) - (raw_list[1][1]), 2))
                
                if (d + small_d) >= i:
                    q_x = (raw_list[0][0]) + ((i-d) / small_d) * ((raw_list[1][0]) - (raw_list[0][0]))
                    q_y = (raw_list[0][1]) + ((i-d) / small_d) * ((raw_list[1][1]) - (raw_list[0][1]))
                    resampled_list.append((q_x, q_y))
                    raw_list.pop(0)
                    raw_list.insert(0, (q_x, q_y))
                    d = 0
                else:
                    raw_list.pop(0)
                    d += small_d
            
            if len(resampled_list) < self.N_RESAMPLE_POINTS:
                resampled_list.append(raw_list[0])
            
            for point in resampled_list:
                self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="red")

            self.text.insert("4.0", ", Resampled into N=" + str(len(resampled_list)))
            
            return resampled_list

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
        Clear the canvas.
        """
        self.canvas.delete("all")
        self.raw_input_points.clear()
