#!/usr/bin/env python3

"""
 Draws a single just like line.py but does so
 using a 'random' character
"""

from asciiWriter.patterns import vertical
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import random, space

# Set the canvas
width = 75
height = 75

# Define the line, most importantly it's position
image_pattern = vertical(20)
# We're going to fill the line with random selections
# from the '%$&@!*' chars
mark = random('%$&@!*')
# Set the character for the 'blank'  space
blank = space()

# Make a canvas
lines = make_lines(width, height)
# Draw the result
result = visit(lines, image_pattern, mark, blank)

# Print the result
print_lines(result)