"""
ResultFilter.py

Filter the incoming stream so it only
contains MatchResults of the specified types.
"""
from MatchResult import MatchResult

class ResultFilter(object):
  """
  Defines a callable object that filters a given stream.

  >>> mr1 = MatchResult("NP")
  >>> mr1["cn"] = "dog"
  >>> mr2 = MatchResult("VP")
  >>> mr2["subj"] = mr1
  >>> mr2["v"] = "barks"
  >>> tstream = ["the", "dog", mr1, "barks", mr2]
  >>> rf = ResultFilter(["VP"])
  >>> list(rf(tstream))
  [VP{'subj': NP{'cn': 'dog'}, 'v': 'barks'}]

  """

  def __init__(self, types):
    self._types = types
    super(ResultFilter, self).__init__()

  def __call__(self, gen):
    for tok in gen:
      if isinstance(tok, MatchResult):
        if tok.token_type in self._types:
          yield tok

# Doctest magic
if __name__ == '__main__':
  import doctest
  doctest.testmod()
