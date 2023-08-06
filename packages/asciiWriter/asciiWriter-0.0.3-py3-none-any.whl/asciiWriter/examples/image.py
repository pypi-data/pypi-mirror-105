#!/usr/bin/env python3

"""
  Uses an image as a guide to draw either blanks or
  mark chars. In this case with the char '+'.
"""

from asciiWriter.patterns import image
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import single, space

from os.path import join, dirname

width = 75
height = 75

# Where to find the image
image_path = join(dirname(__file__), 'data', 'blobs-small.png')
# Construct the pattern
image_pattern = image(image_path)
# Set the marker, in this case the character '+'
mark = single('+')
# Define what to use on a blank space, as a variation you could use: single('*')
blank = space()

# Make a canvas
lines = make_lines(width, height)
# Draw the picture
result = visit(lines, image_pattern, mark, blank)

# Print the result
print_lines(result)