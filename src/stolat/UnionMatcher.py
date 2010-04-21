"""
UnionMatcher.py

Implements a matcher that matches a set of sub-matchers.
"""

from Matcher import Matcher

class UnionMatcher(Matcher):
  """
  A matcher that matches a set of sub-matchers.
  """

  def __init__(self, submatchers):
    self._submatchers = submatchers
    maxlength = max(submatchers, key=lambda x: x._buffer_length)._buffer_length
    super(UnionMatcher, self).__init__(buffer_length = maxlength)

  def __or__(self, other):
    """
    Special version to cope with chains of unions.

    >>> m = Matcher('dog') | Matcher('cat') | Matcher('mouse')
    >>> len(m._submatchers)
    3

    >>> list(m("the dog chases the cat chases the mouse".split()))
    ['the', 'dog', dog{'token': 'dog'}, 'chases', 'the', 'cat', cat{'token': 'cat'}, 'chases', 'the', 'mouse', mouse{'token': 'mouse'}]
    """
    submatchers = self._submatchers + [other]
    return UnionMatcher(submatchers)

  def _match(self, buf):
    """
    Matches all the submatchers in parallel.

    >>> m1 = Matcher("dog", "animal")
    >>> m2 = Matcher("cat", "animal")
    >>> m = UnionMatcher([m1,m2])
    >>> list(m("the dog chases the cat".split()))
    ['the', 'dog', animal{'token': 'dog'}, 'chases', 'the', 'cat', animal{'token': 'cat'}]
    """
    results = []
    for m in self._submatchers:
      results += m._match(buf)
    return results

# Doctest magic
if __name__ == '__main__':
  import doctest
  doctest.testmod()
