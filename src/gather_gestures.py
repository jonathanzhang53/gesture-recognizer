import sys

from canvas import Canvas

def str2bool(v: str) -> bool:
    return v.lower() in ("yes", "true", "t", "1")
try:
    sys.argv[1] = str2bool(sys.argv[1])
except IndexError:
    sys.argv.append(False)

if __name__ == "__main__":
    canvas = Canvas(sys.argv)
    """ 
    Takes the following arguments:
        1. Gather mode (True/False)
        2. Username (string) (optional)
        3. Sample # to resume at (int) (optional)
    """
    canvas.run()