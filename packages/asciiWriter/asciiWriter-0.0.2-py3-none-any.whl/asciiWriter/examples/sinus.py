#!/usr/bin/env python3

from asciiWriter.patterns import sinus_vertical
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import sentence, space, single

# Define width and height of the output
width = 75
height = 75

# Set the pattern we use to draw, in this case a
# sinoid, with period of 40 lines, and an amplitude
# of 30 characters. Slightly less than half our canvas width
pattern = sinus_vertical(period=40, amplitude=30)
# We use a sentence to draw the text
mark = sentence('OPEN DESIGN COURSE ')
# Define a blank character
blank = single(' ')

# Make the canvas
lines = make_lines(width, height)

# Draw the sinoid
result = visit(lines, pattern, mark, blank)

# Output the result
print_lines(result)