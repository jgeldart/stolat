"""
MatchResult.py

A dictionary subclass that adds some extra fields relevant to matches.
"""

class MatchResult(dict):
  """
  A dictionary-like object that holds information relevant to matches.
  """

  def __init__(self, token_type):
    """
    Create a new MatchResult. 
    """
    self._token_type = token_type
    super(MatchResult, self).__init__()

  def _get_token_type(self):
    return self._token_type

  def _set_token_type(self, token_type):
    if token_type is not None:
      self._token_type = token_type

  token_type = property(_get_token_type, _set_token_type)

  def __repr__(self):
    """
    Return a meaningful representation of this match result.

    >>> mr = MatchResult("date")
    >>> mr["year"] = 2010
    >>> mr
    date{'year': 2010}
    """
    return "%s%s"%(self.token_type, super(MatchResult, self).__repr__())

# Doctest magic invocations
if __name__ == "__main__":
  import doctest
  doctest.testmod()
