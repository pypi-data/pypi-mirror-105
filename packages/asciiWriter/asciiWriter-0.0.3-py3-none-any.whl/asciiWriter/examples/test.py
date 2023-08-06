#!/usr/bin/env python3

from asciiWriter.patterns import sinus_vertical, cross
from asciiWriter.utils import make_lines, visit, print_lines, merge
from asciiWriter.marks import sentence, space, single

# Define width and height of the output
width = 100
height = 50

# As we draw multiple sinoids we will collect
# them in a list of layers
layers = []

# Loop through an offset from -40 to 40 in steps of 10
for x in range(-50, 50, 10):
    
  # Set the pattern with the changing offset
  pattern = cross()
  # We use a sentence to draw the text
  mark = sentence('Hello World! ')
  # Define a blank character
  blank = single('-')

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
