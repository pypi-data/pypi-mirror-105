#!python

from asciiWriter.patterns import sinus_vertical
from asciiWriter.utils import make_lines, visit, print_lines, merge
from asciiWriter.marks import sentence, space

# Define width and height of the output
width = 75
height = 75

# As we draw multiple sinoids we will collect
# them in a list of layers
layers = []

# Loop through an offset from -40 to 40 in steps of 10
for x in range(-40, 40, 10):
  # Set the pattern with the changing offset
  pattern = sinus_vertical(period=40, amplitude=30, offset=x)
  # We use a sentence to draw the text
  mark = sentence('OPEN DESIGN COURSE ')
  # Define a blank character
  blank = space()
  
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
