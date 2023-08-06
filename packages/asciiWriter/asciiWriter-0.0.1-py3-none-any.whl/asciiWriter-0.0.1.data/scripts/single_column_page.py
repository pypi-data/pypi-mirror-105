#!python

from asciiWriter.text import make_column, make_multi_column
from asciiWriter.utils import merge, print_lines, make_lines, translate
from hyphen import Hyphenator
import math

# Define width and height of the output
width = 100
height = 500

# Import a text
text = open('texts/language.txt').read()

# Import a hyphenator
h_en = Hyphenator('en_US')

# Make an empty layers list
layers = []

def sin_width (line_nr, _):
  amplitude = 25
  period = 150 / (math.pi * 2)

  return 50 + math.floor(math.sin(line_nr / period) * amplitude)

def cos_width (line_nr, _):
  amplitude = 5
  period = 20 / (math.pi * 2)
  half_amplitude = amplitude * .5

  return math.floor(half_amplitude + math.cos(line_nr / period) * half_amplitude)

# Transform the text into a column
lines, remaining = make_column(text, height=height, use_hyphenator=h_en, line_width=sin_width, line_offset=cos_width)

# Transform the text into multiple columns
# lines, remaining = make_multi_column(text, height=height-3, use_hyphenator=h_en)
lines = translate(lines, x=15, y=1)

# Create an background
background = make_lines(width, height, ' ')

# Add all your layers to the layers list
layers.append(background)
layers.append(lines)

# Merge the layers into one layer again
merged = merge(width, height, ' ', layers)

# Print the result
print_lines(merged)
