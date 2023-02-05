import tkinter as tk
import math
import StoredGestures

raw_input_points = [] #Contains the raw points for the user's currently drawn gesture

"""
Determines the total length of a given list of points.
"""
def PathLength(A):
    small_d = 0
    for i in range(1, len(A)):
        # Distance = sqrt(a^2 + b^2) = sqrt((x2-x1)^2+(y2-y1)^2)
        small_d += (math.sqrt(math.pow((A[i][0])-(A[i-1][0]),2)+math.pow((A[i][1])-(A[i-1][1]),2)))
    return small_d

"""
Resamples the given list of points into N evenly spaced points.
"""
def Resample():
    raw_list = raw_input_points
    N = min(64, len(raw_list)-1)
    if len(raw_list) > 1:
        I = PathLength(raw_list)/(N-1)
        D = 0
        resampled_list = []
        resampled_list.append(raw_list[0])
        i = 1
        while i <= len(raw_list)-1:
            small_d = math.sqrt(math.pow((raw_list[i-1][0])-(raw_list[i][0]),2)+math.pow((raw_list[i-1][1])-(raw_list[i][1]),2))
            if (D + small_d) >= I:
                q_x = (raw_list[i-1][0]) + ((I-D)/small_d) * ((raw_list[i][0]) - (raw_list[i-1][0]))
                q_y = (raw_list[i-1][1]) + ((I-D)/small_d) * ((raw_list[i][1]) - (raw_list[i-1][1]))
                resampled_list.append((q_x,q_y))
                raw_list.insert(1,(q_x,q_y))
                i += 1
                D = 0
            else:
                i += 1
                D += small_d
        for point in resampled_list:
            canvas.create_oval(point[0]-3, point[1]-3, point[0]+3, point[1]+3, fill="red")
        return resampled_list


""" 
Draw on the canvas with the mouse.
MouseDown (start of input), MouseDragged (input continues), and MouseUp (input ends).
"""
def paint(event):
    x1, y1 = (event.x - 1.5), (event.y - 1.5)
    x2, y2 = (event.x + 1.5), (event.y + 1.5)
    canvas.create_oval(x1, y1, x2, y2, fill="black")
    raw_input_points.append((event.x,event.y))

"""
Clear the canvas.
"""
def clear_canvas():
    canvas.delete("all")
    raw_input_points.clear()

# ROOT WINDOW
root = tk.Tk()
root.title("My Canvas")

# CANVAS
canvas = tk.Canvas(root, width=300, height=200)
canvas.config(bg='gray')
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# CLEAR BUTTON
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack()

# DEBUG: RESAMPLE BUTTON
debug_resample_button = tk.Button(root, text="DEBUG: resample", command=Resample)
debug_resample_button.pack()

# MAIN LOOP
root.mainloop()