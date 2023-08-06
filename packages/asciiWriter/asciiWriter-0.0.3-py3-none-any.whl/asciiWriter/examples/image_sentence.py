#!/usr/bin/env python3

"""
  Uses an image to define where to put chars.
  In this case with the sentence/word ASCII
"""

from asciiWriter.patterns import image
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import sentence, space

from os.path import join, dirname

width = 75
height = 75

# Where to find the image
image_path = join(dirname(__file__), 'data', 'shapes.png')
# Construct the pattern
image_pattern = image(image_path)
# Set the marker, in this case a sentence
mark = sentence('U.R.S O.P.E.N.  D.E.S.I.G.N  C.O.')
# Define what to use on a blank space, as a variation you coul use: single('*')
blank = space()

# Make a canvas
lines = make_lines(width, height)
# Draw the picture
result = visit(lines, image_pattern, mark, blank)

# Print the result
print_lines(result)