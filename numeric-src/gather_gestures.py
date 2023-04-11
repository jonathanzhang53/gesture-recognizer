# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

from canvas import Canvas

import sys


if __name__ == "__main__":
    canvas = Canvas(sys.argv)
    """ 
    Takes the following arguments:
        1. Gather mode (string) ("1dollar"/"numeric")
        2. Username (string) (optional)
        3. Sample # to resume at (int) (optional)
    """
    canvas.run()
