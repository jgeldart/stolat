"""
RegexpPattern.py

Implements a pattern that matches a given regexp.
"""

import re as RE

from Pattern import Pattern
from MatchResult import MatchResult

class RegexpPattern(Pattern):
  """
  A pattern that matches the given regexp.
  """

  def __init__(self, regexp, type_name = None):
    self.regexp = RE.compile(regexp)

    self.type_name = type_name
    super(RegexpPattern, self).__init__()

  def matches(self, buf):
    """
    Searches for a token in the buffer which matches the given regexp.
    
    >>> buf = "the price was $120.35".split()
    >>> buf.reverse()
    >>> (Pattern('price') + RegexpPattern('\$\d+(\.\d{2})?')%'amt').matches(buf)
    ({'amt': '$120.35'}, ['the'])

    We can use named groups to create a MatchResult object out of the data
    >>> (Pattern('price') + RegexpPattern('\$(?P<dollars>\d+)(\.(?P<cents>\d{2}))?')%'amt').matches(buf)
    ({'amt': Amt{'cents': '35', 'dollars': '120', '_match': '$120.35'}}, ['the'])

    We can also explicitly set a type name for the produced MatchResult
    >>> (Pattern('price') + RegexpPattern('\$(?P<dollars>\d+)(\.(?P<cents>\d{2}))?', 'CUREX')%'amt').matches(buf)
    ({'amt': CUREX{'cents': '35', 'dollars': '120', '_match': '$120.35'}}, ['the'])

    """
    buf_length = len(buf)
    for i in range(buf_length):
      if not isinstance(buf[i], MatchResult):
        ms = self.regexp.match(str(buf[i]))
        if ms is not None:
          # Do we have named groups? If so, build a dictionary of them
          if len(self.regexp.groupindex) > 0:
            # If we don't have an explicit name for the MatchResult, calculate one from the field name
            tname = self.type_name
            if tname is None:
              tname = self.field.capitalize()
            # Copy the groups into a MatchResult object
            result = MatchResult(tname)
            result['_match'] = ms.group(0)
            for k,n in self.regexp.groupindex.items():
              # If the group isn't none in this instance
              if ms.group(n) is not None:
                result[k] = ms.group(n)
            return result, buf[i+1:]
          else:
            if self.field is not None:
              rd = {}
              rd[self.field] = ms.group(0)
              return rd, buf[i+1:]
            else:
              return ms.group(0), buf[i+1:]
    return None, []

re = RegexpPattern

# Doctest magic
if __name__ == "__main__":
  import doctest
  doctest.testmod()
