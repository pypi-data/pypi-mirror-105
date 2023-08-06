"""
  Based on the textwrap2 module included in the PyHyphen library:
  https://pypi.org/project/PyHyphen
"""

import textwrap

class TextWrapper(textwrap.TextWrapper):
    """
    This class extends the Python 3 standard library's TextWrapper and adds an optional
    use_hyphenator to its constructor arguments.
    """

    def __init__(self, *args, **kwargs):
        self.use_hyphenator = kwargs.pop("use_hyphenator", None)
        super().__init__(*args, **kwargs)

    def _wrap_chunks(self, chunks):

        lines = []
        if (chunks):
          """Override the mother class method.

          Most of that method is directly copied from the original class, except
          for the part with use_hyphenator.
          """
          if self.width <= 0:
              raise ValueError("invalid width %r (must be > 0)" % self.width)
          if self.max_lines is not None:
              if self.max_lines > 1:
                  indent = self.subsequent_indent
              else:
                  indent = self.initial_indent
              if len(indent) + len(self.placeholder.lstrip()) > self.width:
                  raise ValueError("placeholder too large for max width")

          # Arrange in reverse order so items can be efficiently popped
          # from a stack of chucks.
          chunks.reverse()

          # Start the list of chunks that will make up the current line.
          # cur_len is just the length of all the chunks in cur_line.
          cur_line = []
          cur_len = 0

          # Figure out which static string will prefix this line.
          if lines:
              indent = self.subsequent_indent
          else:
              indent = self.initial_indent

          # Maximum width for this line.
          width = self.width - len(indent)

          # First chunk on line is whitespace -- drop it, unless this
          # is the very beginning of the text (ie. no lines started yet).
          if self.drop_whitespace and chunks[-1].strip() == '' and chunks[-1][0] != '\n': # and lines:
              del chunks[-1]

          while chunks:
              l = len(chunks[-1])

              # Check for a newline character
              if chunks[-1] == '\n':
                  return indent + ''.join(cur_line), ''.join(reversed(chunks[:-1]))
              elif chunks[-1][0] == '\n':
                  return indent + ''.join(cur_line), ''.join(reversed(chunks[:-1] + [chunks[-1][1:]]))

              # Can at least squeeze this chunk onto the current line.
              if cur_len + l <= width:
                  cur_line.append(chunks.pop())
                  cur_len += l

              # Nope, this line is full.
              # But try hyphenation.
              else:
                  if self.use_hyphenator and (width - cur_len >= 2):
                      hyphenated_chunk = self.use_hyphenator.wrap(chunks[-1], width - cur_len)
                      if hyphenated_chunk:
                          cur_line.append(hyphenated_chunk[0])
                          chunks[-1] = hyphenated_chunk[1]

                  break

          # The current line is full, and the next chunk is too big to
          # fit on *any* line (not just this one).
          if chunks and len(chunks[-1]) > width:
              self._handle_long_word(chunks, cur_line, cur_len, width)
              cur_len = sum(map(len, cur_line))

          # If the last chunk on this line is all whitespace, drop it.
          if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
              cur_len -= len(cur_line[-1])
              del cur_line[-1]

          if cur_line:
              if (self.max_lines is None or
                  len(lines) + 1 < self.max_lines or
                  (not chunks or
                    self.drop_whitespace and
                    len(chunks) == 1 and
                    not chunks[0].strip()) and cur_len <= width):
                  # Convert current line back to a string and store it in
                  # list of all lines (return value).
                  return indent + ''.join(cur_line), ''.join(reversed(chunks))
              else:
                  while cur_line:
                      if (cur_line[-1].strip() and
                          cur_len + len(self.placeholder) <= width):
                          cur_line.append(self.placeholder)
          
                          return indent + ''.join(cur_line), ''.join(reversed(chunks))

                      cur_len -= len(cur_line[-1])
                      del cur_line[-1]
                  else:
                      if lines:
                          prev_line = lines[-1].rstrip()
                          if (len(prev_line) + len(self.placeholder) <=
                                  self.width):
                              lines[-1] = prev_line + self.placeholder
                              
                  return indent + self.placeholder.lstrip(), ''.join(reversed(chunks))
        else:
          return '', ''
          
def wrap_single_line (text, width=70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)

if __name__ == '__main__':
    from hyphen import Hyphenator
    h_en = Hyphenator('en_US')

    line, remaining = wrap_single_line('https://stackoverflow.com/questions/3940128/how-can-i-reverse-a-list-in-python', width=46, use_hyphenator=h_en)

    print(line, remaining)