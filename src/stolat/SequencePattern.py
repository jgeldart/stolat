"""
SequencePattern.py

Take a list of patterns and apply them in sequence.
"""
from Pattern import Pattern

class SequencePattern(Pattern):
  """
  A pattern that matches a list of sub-patterns
  """

  def __init__(self, subpatterns, field = None):
    self.subpatterns = subpatterns
    super(SequencePattern, self).__init__("", field=field)

  def matches(self, buf):
    """
    Iterate binding subpatterns where possible.
    """
    result = {}
    cur_buf = [t for t in buf]
    for p in self.subpatterns:
      r, rest = p.matches(cur_buf)
      cur_buf = rest

      # Do we have a result for this subpattern?
      if r is None:
        return None, cur_buf

      # If this subpattern has a field associated, bind it in the result
      if p.field and not p.field in result.keys():
        result[p.field] = r

    return result, cur_buf

  def __add__(self, other):
    """
    Special case for chaining pattern sequences.

    >>> p = Pattern("the") + Pattern("dog") + Pattern("chases")
    >>> len(p.subpatterns)
    3
    
    >>> p.matches(["cat","the","chases","dog","the"])
    ({}, [])
    """
    subpats = [other] + self.subpatterns 
    return SequencePattern(subpats)

  def __len__(self):
    """
    Return the length of this pattern, defined as the number of
    subpatterns.

    >>> len(SequencePattern([Pattern("the"),Pattern("dog")]))
    2
    """
    return len(self.subpatterns)

# Doctest magic
if __name__ == "__main__":
  import doctest
  doctest.testmod()
