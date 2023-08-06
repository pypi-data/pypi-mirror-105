# -*- coding: utf-8 -*-
from .wrap_single_line import wrap_single_line
from .utils import translate, merge

def make_column(text, line_width=50, height=200, use_hyphenator=None, line_offset=0):
    
  lines = []
  remaining = text

  while remaining and len(lines) < height:

      if callable(line_width):
          width = line_width(len(lines), height)
      else:
          width = line_width

      if callable(line_offset):
          offset = line_offset(len(lines), height)
      else:
          offset = line_offset 

      line, remaining = wrap_single_line(remaining, width, use_hyphenator=use_hyphenator, replace_whitespace=False, drop_whitespace=True)
  
      line = list(line)

      if offset != 0:
        line = [None for _ in range(offset)] + line

      lines.append(line)
  
  return lines, remaining

def make_multi_column(text, height=200, column_width=40, column_count=2, column_gap=5, use_hyphenator=None, space_char=None):
  # todo: vertical offset?
  
  remaining = text 
  i = 0

  columns = []

  while remaining and i < column_count:
    column, remaining = make_column(remaining, line_width=column_width, height=height, use_hyphenator=use_hyphenator)
    if i > 0:
      offset = (column_width + column_gap) * i
      column = translate(column, x=offset, y=0)
    columns.append(column)
    i += 1

  width = (column_width + column_gap) * column_count
  lines = merge(width, height, space_char, columns)
  return lines, remaining


if __name__ == '__main__':
  print(make_column('Hello world!', line_width=25, height=10))