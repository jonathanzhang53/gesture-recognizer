import sys

from canvas import Canvas

def str2bool(v: str) -> bool:
    return v.lower() in ("yes", "true", "t", "1")

if __name__ == "__main__":
    canvas = Canvas(str2bool(sys.argv[1]))
    canvas.run()