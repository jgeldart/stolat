"""
TokenPattern.py

Implements a pattern that matches a MatchResult in the stream. Use to
simulate recursion.
"""
from Pattern import Pattern
from MatchResult import MatchResult

class TokenPattern(Pattern):

  def __init__(self, token_type):
    self.token_type = token_type
    super(TokenPattern, self).__init__()

  def matches(self, buf):
    """
    Match the buffer against a particular token type.

    >>> buf = ['away', 'ran', mr, 'dog', 'the']
    >>> TokenPattern('CN').matches(buf)
    (CN{'noun': 'dog'}, ['dog', 'the'])
    """
    buf_length = len(buf)
    for i in range(buf_length):
      t = buf[i]
      if isinstance(t, MatchResult):
        if t.token_type == self.token_type:
          return t, buf[i+1:]
    return None, []

token = TokenPattern

# Doctest magic
if __name__ == '__main__':
  import doctest
  doctest.testmod()
