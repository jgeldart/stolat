"""
Pattern.py

Implements a pattern to be matched by a matcher.
"""

from PatternMatcher import PatternMatcher

class Pattern(object):
  """
  A pattern to be matched by an object.

  <<< (word("price") + regexp("$\d+(\.\d{2})")%"amount") >> "PRICE"
  """

  def __init__(self, pattern="", field = None):
    self.pattern = pattern
    self.field = field
    super(Pattern, self).__init__()

  def matches(self, buf):
    """
    Match a single word from the buffer consuming the prior portion
    greedily.

    >>> buf = "the dog ran away".split()
    >>> buf.reverse()
    >>> Pattern("dog").matches(buf)
    ('dog', ['the'])
    """
    buf_length = len(buf)
    for i in range(buf_length):
      if buf[i] == self.pattern:
        return buf[i], buf[i+1:]
    return None, []

  def __len__(self):
    """
    Returns the length of the pattern, used to compute the minimum
    buffer size necessary to match this pattern.

    >>> len(Pattern("word"))
    1
    """
    return 1

  def __add__(self, other):
    """
    Take two patterns and combine them in sequence.

    >>> buf = "the dog ran away".split()
    >>> buf.reverse()
    >>> (Pattern("the") + Pattern("dog")).matches(buf)
    ({}, [])

    Try with setting a field:
    >>> (Pattern("the",field="determiner") + Pattern("dog")).matches(buf)
    ({'determiner': 'the'}, [])
    """
    from SequencePattern import SequencePattern
    return SequencePattern([other, self])

  def __mod__(self, other):
    """
    Bind this pattern to the given field name.

    >>> buf = "the dog ran away".split()
    >>> buf.reverse()
    >>> (Pattern("the")%"determiner" + Pattern("dog")).matches(buf)
    ({'determiner': 'the'}, [])

    And with two patterns to bind:
    >>> (Pattern("the")%"determiner" + Pattern("dog")%"noun").matches(buf)
    ({'noun': 'dog', 'determiner': 'the'}, [])
    """
    self.field = other
    return self

  def __rshift__(self, other):
    """
    Turn this pattern into a PatternMatcher with the given typename.

    >>> matchr = (Pattern("the") + Pattern("dog")%"noun") >> "CN"
    >>> list(matchr("the dog ran away".split()))
    ['the', 'dog', CN{'noun': 'dog'}, 'ran', 'away']

    >>> buf = "the dog ran away".split()
    >>> buf.reverse()
    >>> (Pattern("the") + Pattern("dog")%"noun").matches(buf)
    ({'noun': 'dog'}, [])
    """
    return PatternMatcher(self, other)

word = Pattern

# Doctest magic
if __name__ == "__main__":
  import doctest
  doctest.testmod()
