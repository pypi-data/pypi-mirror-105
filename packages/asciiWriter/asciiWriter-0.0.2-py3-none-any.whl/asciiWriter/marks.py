from random import choice
from string import ascii_letters

def random (marks=ascii_letters):
  """Random mark from provided marks."""
  def func ():
    return choice(marks)

  return func

def sentence (mark_text):
  """Deprecated. Use text."""
  return text(mark_text)

def text (mark_text):
  """Loops through provided text."""
  chars = list(mark_text)
  def f():
    char = chars.pop(0)
    chars.append(char)
    return char
  return f
 
def single (char=' '):
  """Mark with a single character."""
  def f():
    return char

  return f

def space (space=' '):
  """Convenience function to mark with spaces."""
  return single(space)
