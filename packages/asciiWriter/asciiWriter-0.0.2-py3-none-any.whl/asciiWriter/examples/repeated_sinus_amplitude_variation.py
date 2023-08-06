#!/usr/bin/env python3

from asciiWriter.patterns import sinus_vertical
from asciiWriter.utils import make_lines, visit, print_lines, merge, translate
from asciiWriter.marks import sentence, space

import random

# Define width and height of the output
width = 125
height = 90

# As we draw multiple sinoids we will collect
# them in a list of layers
layers = []

# Loop through an amplitude of -50 to 50 in steps of 10
for amplitude in range(-40, 50, 10):
  # Set the pattern with the changing amplitude
  pattern = sinus_vertical(period=60, amplitude=amplitude)
  # We use a sentence to draw the text
  mark = sentence('VARIA-')
  # Define a blank character
  blank = space('-')

  # Make the canvas
  lines = make_lines(width, height)
  # Draw the sinoid, but add it to the list
  result = visit(lines, pattern, mark, blank)
  # Add it the result to the list of layers
  layers.append(result)

# Merge the layers into one layer again
merged = merge(width, height, blank(), layers)

# Print the result
print_lines(merged)
