#!/usr/bin/env python3

"""
 Draws lines like line.py, but draws more than one
"""

from asciiWriter.patterns import vertical
from asciiWriter.utils import make_lines, visit, print_lines, merge
from asciiWriter.marks import sentence, space

# Set the canvas
width = 75
height = 75

# We are going to draw multiple lines and collect them
# in a list named 'layers'
layers = []

# Set the position of the line, do this in a loop
# from 10 to 75 in steps of then
for x in range(10, 75, 10):
  # Define the line, x will start at 10 and grow in steps of 10
  image_pattern = vertical(x)
  # Fill the line with the sentence 'OPEN DESIGN COURSE '
  mark = sentence('OPEN DESIGN COURSE ')
  # Set the blank space
  blank = space()

  # Make a canvas
  lines = make_lines(width, height)
  # Make a layer with the line
  layer = visit(lines, image_pattern, mark, blank)
  # Add the layer to the list of layers
  layers.append(layer)

# Merge the list of layers into a single layer
result = merge(width, height, blank(), layers)
# Print the result
print_lines(result)