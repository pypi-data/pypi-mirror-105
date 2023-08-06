#!python

"""
 Draws a single, vertical line
"""

from asciiWriter.patterns import vertical
from asciiWriter.utils import make_lines, visit, print_lines
from asciiWriter.marks import sentence, space

# Set the canvas
width = 75
height = 75

# Define the line, most importantly it's position
pattern = vertical(20)
# We're going to fill the line with a text
mark = sentence('OPEN DESIGN COURSE ')
# Set the character for the 'blank' space
blank = space()

# Make a canvas
lines = make_lines(width, height)
# Draw the result
result = visit(lines, pattern, mark, blank)

# Print the result
print_lines(result)