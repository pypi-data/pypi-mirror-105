import math

# # Linear
def diagonal():
  def f (x, y, width, height, mark, blank):
    if x == math.floor((y / float(height)) * width):
      return mark()
    else:
      return blank()

  return f

# Cross
def cross ():
  def f (x, y, width, height, mark, blank):
    pos = math.floor((y / float(height)) * width)

    if x == pos or (width - 1) - pos == x:
      return mark()
    else:
      return blank()
  return f

def horizontal (position):
  def f (x, y, width, height, mark, blank):
    return mark() if position == y else blank()
  return f

def vertical (position):
  def f (x, y, width, height, mark, blank):
    return mark() if position == x else blank()
  return f

# Sinus
def sinus_vertical (period=0.2, amplitude=0.5, offset_t=0, offset=0):
  period = (period / (math.pi * 2))
  
  def f (x, y, width, height, mark, blank):
    middle = (width - 1) * .5
    to_mark = math.floor(middle + math.sin(offset_t + y / period) * amplitude)
    return mark() if (x + offset) == to_mark else blank()
  return f

def sinus_horizontal (period=0.2, amplitude=0.5, offset_t=0, offset=0):
  period = (period / (math.pi * 2))
  def f (x, y, width, height, mark, blank):
    middle = (height - 1) * .5
    to_mark = math.floor(middle + math.sin(offset_t + x / period) * amplitude)
    return mark() if y + offset == to_mark else blank()

  return f

def image (path, threshold=128):
  from PIL import Image

  im = Image.open(path).convert('L')
  image_width, image_height = im.size
  pixels = im.load()

  def f (x, y, width, height, mark, blank):
    if x < image_width and y < image_height:
      if pixels[x, y] < threshold:
        return mark()

    return blank()
  
  return f
