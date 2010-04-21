"""
Corrector.py

Implements Peter Norvig's statistical spelling corrector; used as part of the
normalisation process.

See http://norvig.com/spell-correct.html for more information.
"""
import collections

class Corrector(object):
  """
  Implements a spelling corrector using a table of conditional edit
  probabilities supplied in the constructor.
  """

  def __init__(self, corpus, smoothing = 1): 
    """
    Create a new spelling correction callable object. Pass in a corpus; a
    sequence of words.

    Takes an optional smoothing parameter that indicates the minimum
    frequency of any item whether or not it is in the corpus. This defaults
    to 1.

    >>> Corrector("the dog hit the cat".split())
    Corrector: 4 unique words, alphabet: 9
    """
    self._corpus = collections.defaultdict(lambda: smoothing)
    self._alphabet = set()
    for w in corpus:
      self._corpus[w] += 1
      # Build the alphabet set from the corpus progressively to allow larger corpora
      self._alphabet = self._alphabet.union(set(c for c in w))    

    super(Corrector, self).__init__()

  def __call__(self, gen):
    """
    Takes a generator that yields a sequence of strings and produces a
    generator that yields a sequence of automatically corrected strings.

    >>> cor = Corrector("the dog hit the cat".split())
    >>> list(cor("teh dog hut the cat".split()))
    ['the', 'dog', 'hit', 'the', 'cat']
    """
    for tok in gen:
      yield self._correct(tok)

  def __repr__(self):
    """
    Return a string representation of the corrector instance.
    """
    return "Corrector: %d unique words, alphabet: %d"%(len(self._corpus), len(self._alphabet))

  def _correct(self, word):
    """
    Return the most likely correction for the given word.
    """
    candidates = self._known([word]) or self._known(self._edits1(word)) or self._known_edits(word) or [word]
    return max(candidates, key=self._corpus.get)

  def _known(self, words):
    """
    Return the set of known words in the provided sequence.
    """
    return set(w for w in words if w in self._corpus)

  def _known_edits(self, word):
    """
    Return the set of known words out of all words within edit distance 2 of the provided word.
    """
    return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1) if e2 in self._corpus)

  def _edits1(self, word):
    """
    Return the set of words within edit distance 1 of the provided word.
    """
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in self._alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in self._alphabet]
    return set(deletes + transposes + replaces + inserts)

# Doctest magic invocation
if __name__ == "__main__":
  import doctest
  doctest.testmod()
