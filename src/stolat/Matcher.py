"""
Matcher.py

A basic matcher class. A matcher is a callable object that takes a generator
and returns a generator that augments the stream wih additional elements.

The matcher implemented here simply looks for strings, and binds them to an 
output MatchToken.
"""

from MatchResult import MatchResult

class Matcher(object):
  """
  A Matcher takes a stream of tokens to a stream of tokens, augmenting them
  along the way when a match is found.
  """

  def __init__(self, pattern = None, match_type = None, buffer_length = 1, keep_original = True):
    """
    Create a new matcher that matches simple strings and lifts them to a
    MatchResult. The type of the MatchResult defaults to the pattern, and the
    buffer length to 1.

    If keep_original is set to False, the matcher will only pass positive
    matches onwards; the original tokens will be dropped.
    """
    self._pattern = pattern

    if match_type is None:
      match_type = pattern
    self._match_type = match_type

    self._keep_original = keep_original

    self._buffer_length = buffer_length
    self._buffer = []

    self._forwardbuffer = []

  def __xor__(self, other):
    """
    Boost the buffer length for this matcher. Use to allow 'gapping' and
    unrecognised tokens.

    >>> m = Matcher('dog') ^ 3
    >>> m._buffer_length
    4
    """
    self._buffer_length += other
    return self

  def __or__(self, other):
    """
    Combine two matchers into a union matcher that runs both in parallel.

    >>> m = Matcher('dog', 'animal') | Matcher('cat', 'animal')
    >>> list(m("the dog chases the cat".split()))
    ['the', 'dog', animal{'token': 'dog'}, 'chases', 'the', 'cat', animal{'token': 'cat'}]

    The buffer length combines to give the maximum of the matchers:
    >>> m._buffer_length
    1

    And the length changes with boosts:
    >>> m = Matcher('dog')^3 | Matcher('cat')^1
    >>> m._buffer_length
    4
    """
    from UnionMatcher import UnionMatcher
    return UnionMatcher([self,other])

  def __call__(self, gen):
    """
    Apply this matcher to the given generator stream.

    >>> matchr = Matcher("dog")
    >>> list(matchr("the dog and the cat were best of friends".split()))
    ['the', 'dog', dog{'token': 'dog'}, 'and', 'the', 'cat', 'were', 'best', 'of', 'friends']

    Try setting the token type:
    >>> matchr = Matcher("dog", "animal")
    >>> list(matchr("the dog and the cat were best of friends".split()))
    ['the', 'dog', animal{'token': 'dog'}, 'and', 'the', 'cat', 'were', 'best', 'of', 'friends']

    Try turning off pass-through:
    >>> matchr = Matcher("dog", "animal", keep_original=False)
    >>> list(matchr("the dog and the cat were best of friends".split()))
    [animal{'token': 'dog'}]
    """
    for tok in gen:
      forbuf = []
      if self._keep_original:
        yield tok
      
      for r in self._results([tok]):
        yield r
        forbuf.append(r)
      
      for r in self._results(forbuf):
        yield r
        forbuf.append(r)

  def _results(self, toks):
    for tok in toks:
      self._buffer.insert(0, tok)
      # Limit buffer to finite length
      self._buffer = self._buffer[:self._buffer_length]
      for r in self._match(self._buffer):
        yield r

  def _match(self, buf):
    """
    Perform a simple equality match. Override this method in your sub-classes.
    """
    if buf[0] == self._pattern:
      result = MatchResult(self._match_type)
      result["token"] = buf[0]
      return [result]
    else:
      return []

# Doctest magic invocation
if __name__ == "__main__":
  import doctest
  doctest.testmod()
