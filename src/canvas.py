# Python GUI library
import tkinter as tk 

def paint(event):
    """ 
    Draw on the canvas with the mouse.
    MouseDown (start of input), MouseDragged (input continues), and MouseUp (input ends).
    """
    x1, y1 = (event.x - 1.5), (event.y - 1.5)
    x2, y2 = (event.x + 1.5), (event.y + 1.5)
    print("Mousedown: " + str(event.x) + "," + str(event.y))
    canvas.create_oval(x1, y1, x2, y2, fill="black")

def clear_canvas():
    """
    Clear the canvas.
    """
    canvas.delete("all")

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

# MAIN LOOP
root.mainloop()