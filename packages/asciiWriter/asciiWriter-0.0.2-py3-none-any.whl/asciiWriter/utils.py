from sys import stdout

def rotate(layer):
  """ Rotates a layer 90 degrees """
  new_width = len(layer)
  new_height = len(layer[0])
  rotated = [['' for x in range(new_width)] for l in range(new_height)]
  
  for y in range(len(layer)):
    for x in range(len(layer[y])):
      rotated[x][y] = layer[y][x]

  return rotated

def merge(width, height, space_char, layers):
  """Merges given layers in a new grid with given width and height. 
  
  Merges layers into a new grid with the given width and height.
  For each cell the last value is taken, unless it is empty.
  Cells with the provided space char are considered empty.
  """
  output = [[space_char for x in range(width)] for y in range(height)]

  for layer in layers:
    for y in range(min(len(layer), height)):
      for x in range(min(len(layer[y]), width)):
        if layer[y][x] and layer[y][x] != space_char:
          output[y][x] = layer[y][x]

  return output

def make_lines (width, height, fill_char = ''):
  """Deprecated. Use make_layer instead."""
  return make_layer(width, height, fill_char)

def make_layer (width, height, fill_char = ''):
  """Construct a layer with given width and height.
     
     Construct a layer with given width and height.
     If fillchar is provided it is used to fill the grid.
  """
  return [[ fill_char for _ in range(width) ] for __ in range(height)]

def visit (layer, pattern, mark, blank):
  """Apply pattern on the provided layer. Row by row."""
  height = len(layer)
  width = len(layer[0])

  for y in range(height):
    for x in range(width):
      layer[y][x] = pattern(x, y, width, height, mark, blank)

  return layer

def visit_horizontal (layer, pattern, mark, blank):
  """Apply pattern on the provided layer. Column by column."""
  height = len(layer)
  width = len(layer[0])

  for x in range(width):
    for y in range(height):
      layer[y][x] = pattern(x, y, width, height, mark, blank)

  return layer

def print_lines (lines):
  """Deprecated. Use print_layer instead."""
  print_layer(lines, out=stdout)
  
def print_layer(layer, out=stdout):
  """Print / write layer to provided output."""
  for line in layer:
    out.write('{}\n'.format(''.join(line)))

def translate(layer, x=0, y=0, fill_char=None):
  """Translate layer by provided x and y lengths."""
  translated = [[] for _ in range(y)]

  for line in layer:
    translated.append([fill_char for _ in range(x)] + line)

  return translated