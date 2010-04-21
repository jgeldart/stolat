from stolat import *
from stolat.Corrector import Corrector

import re as RE

def words(text): return RE.findall('[a-z]+', text.lower())

corpus = words(file('big.txt').read())

corrector_filter = Corrector(corpus)

# Boosted to cope with skipped words
time_ex = ((word("month") + re("january|february|march|april|may|june|july|august|september|october|november|december")%"month") >> "TIMEX") ^ 3

print "Autocorrection"
print "=============="
print
print list(time_ex("we will be looking to find a new place by the month of febuary and move in by the moonth of march".split()))
print 
print list(time_ex(corrector_filter("we will be looking to find a new place by the month of febuary and move in by the moonth of march".split())))
print

def currency():
  return re("\$(?P<dollars>\d+)(\.(?P<cents>\d{2}))?")

price_ex = ((word("price") + currency() % "amount") >> "PRICEX") ^ 2

print "Regexps"
print "======="
print
print list(price_ex("the price was $23 rather than $24.50 like we told you earlier".split()))
print

det = (word("the") % "determiner") >> "DET"
cn = (re("(cat|dog|mouse)") % "n") >> "CN"
np = (token("DET") + token("CN")%"cn") >> "NP"
vp = (token("NP")%"subj" + re(".+")%"v") >> "VP"
parser = det | cn | np | vp^2

rf = ResultFilter(["VP"])

print "Recursion"
print "========="
print
print list(rf(parser("the black cat miaows".split())))
