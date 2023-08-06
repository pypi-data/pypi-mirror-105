#!/usr/bin/env python3

"""
  Same as image_sentence.py, but rotates the result.
  Uses an image to define where to put chars.
  In this case with the sentence/word ASCII
"""

from asciiWriter.patterns import image
from asciiWriter.utils import make_lines, visit, print_lines, rotate
from asciiWriter.marks import sentence, single

from os.path import join, dirname

width = 75
height = 75

# Where to find the image
image_path = join(dirname(__file__), 'data', 'blobs-small.png')
# Construct the pattern
image_pattern = image(image_path)
# Set the marker, in this case a sentence
mark = sentence('ASCII ')
# Define what to use on a blank space, as a variation you coul use: single('*')
blank = single(' ')

# Make a canvas
lines = make_lines(width, height)
# Draw the picture
result = visit(lines, image_pattern, mark, blank)
# Rotate the canvas
result = rotate(result)
# Print the result
print_lines(result)