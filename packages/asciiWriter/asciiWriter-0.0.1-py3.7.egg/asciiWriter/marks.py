from random import choice

def random (marks=['']):
  def func ():
    return choice(marks)

  return func

def sentence (text):
  chars = list(text)
  def f():
    char = chars.pop(0)
    chars.append(char)
    return char
  return f
 
def single (char):
  def f():
    return char

  return f

def space (space=' '):
  return single(space)
