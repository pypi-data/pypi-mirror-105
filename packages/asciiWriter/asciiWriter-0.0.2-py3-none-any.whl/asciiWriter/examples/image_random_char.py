#!/usr/bin/env python3

from asciiWriter.patterns import image
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import random, single

from os.path import join, dirname

width = 75
height = 75

# Where to find the image
image_path = join(dirname(__file__), 'data', 'blobs-small.png')
# Construct the pattern
image_pattern = image(image_path)
# Set the marker, in this case it makes a random selection from
# the list: +, *, $, #, , 
mark = random(['+', '*', '$', '#', ' ', ' '])
# Define what to use on a blank space, as a variation you coul use: single('*')
blank = single()

# Make a canvas
lines = make_lines(width, height)
# Draw the picture
result = visit(lines, image_pattern, mark, blank)

# Print the result
print_lines(result)