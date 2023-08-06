# -*- coding: utf-8 -*-
from utils import make_lines, merge, print_lines, rotate, visit, visit_horizontal
from patterns import diagonal, horizontal, vertical, sinus_horizontal, sinus_vertical, image
from marks import random_mark, sequence_mark, space
from random import choice, random
import math




# marks = ['┼', '│', '░', '▓', 'X', '■', '≡', '·', '¦', ' ']
# blank = ' '
width = 75
height = 50
mark = sequence_mark('O.P.E.N     D.E.S.I.G.N     C.O.U.R.S.E    ')


layers = []

# layers.append(visit(make_lines(width, height), image('blobs-small.png'), mark, space(' ')))

for offset in range(-50, 50, 15):
  lines = [[] for l in range(height)]
  sinus = sinus_vertical(period=50, amplitude=25, offset=offset, offset_t=random())
  layers.append(visit(make_lines(width, height), sinus, sequence_mark('  K A S K   G E N T  '), space()))

for offset in range(-43, 57, 15):
  lines = [[] for l in range(height)]
  sinus = sinus_vertical(period=40, amplitude=10, offset=offset, offset_t=.5+random())
  layers.append(visit(make_lines(width, height), sinus, mark, space()))

print_lines(merge(width, height, space()(), layers))

# for line in overlay(50, 50, ' ', [rotate(merged), merged]):
#   stdout.write('{}\n'.format(''.join(line)))

# sinus = sinus_horizontal(period=30, amplitude=8)
# for x in range(width):
#   for y in range(height):
#     lines[y].append(sinus(x, y, width, height, mark, space()))

# for line in lines:
#   stdout.write('{}\n'.format(''.join(line)))

# lines = [[draw(x, y, marks) for x in range(width)] for y in range(height)]

# sys.sdout.write('\n'.join([''.join(line) for line in lines]))

# sys.sdout.write('\n'.join([''.join([draw(x, y, marks) for x in range(width)])  for y in range(height)]))
