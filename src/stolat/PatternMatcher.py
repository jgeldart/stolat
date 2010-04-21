"""
PatternMatcher.py

A matcher that takes a pattern and slides it over the input stream,
adding any results to the stream itself.
"""

from Matcher import Matcher
from MatchResult import MatchResult

class PatternMatcher(Matcher):
  """
  A matcher that takes a pattern and slides it over the input stream,
  adding any results to the stream itself.
  """

  def __init__(self, pattern, type_name, keep_original = True):
    super(PatternMatcher, self).__init__(pattern, type_name, len(pattern), keep_original)

  def _match(self, buf):
    """
    """
    rs, remainder = self._pattern.matches(buf)
    if rs is not None:
      r = MatchResult(self._match_type)
      if isinstance(rs, dict):
        for k,v in rs.items():
          r[k] = v
      return [r]
    else:
      return []
