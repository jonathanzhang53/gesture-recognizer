from canvas import Canvas

live = False # True = online mode, False = offline mode.

if __name__ == "__main__":
    canvas = Canvas(live)
    if live:
        canvas.run()
