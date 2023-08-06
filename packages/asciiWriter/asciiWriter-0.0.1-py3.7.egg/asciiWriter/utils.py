from sys import stdout

def rotate(layer):
  new_width = len(layer)
  new_height = len(layer[0])
  rotated = [['' for x in range(new_width)] for l in range(new_height)]
  
  for y in range(len(layer)):
    for x in range(len(layer[y])):
      rotated[x][y] = layer[y][x]

  return rotated

def merge(width, height, space_char, layers):
  output = [[space_char for x in range(width)] for y in range(height)]

  for layer in layers:
    for y in range(min(len(layer), height)):
      for x in range(min(len(layer[y]), width)):
        if layer[y][x] and layer[y][x] != space_char:
          output[y][x] = layer[y][x]

  return output

# Make a multidimensional array
# with the given dimensions
def make_lines (width, height, fill_char = ''):
  return [[ fill_char for _ in range(width) ] for __ in range(height)]

def visit (lines, callback, mark, blank):
  height = len(lines)
  width = len(lines[0])

  for y in range(height):
    for x in range(width):
      lines[y][x] = callback(x, y, width, height, mark, blank)

  return lines

def visit_horizontal (lines, callback, mark, blank):
  height = len(lines)
  width = len(lines[0])

  for x in range(width):
    for y in range(height):
      lines[y][x] = callback(x, y, width, height, mark, blank)

  return lines

def print_lines (lines):
  for line in lines:
    stdout.write('{}\n'.format(''.join(line)))

def translate(shape, x=0, y=0):
  ## TODO implement a negative translation?
  translated = [[] for _ in range(y)]

  for line in shape:
    translated.append([None for _ in range(x)] + line)

  return translated