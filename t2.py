import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

from senticnet.senticnet import Senticnet


# this is arbitrary, and should be better thought out in the future
N_BIGRAMS = 12

headlines = {}
bag_of_words = {}
headline_polarities = {}

def create_bag_of_words(words):
  return dict([word, True] for word in words)

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()

  bad_bad_words = stopwords.words('portuguese')
  word_list = []

  for lines in text:
    values = lines.split(',',4)
    date = (values[2],values[1][1:-1],values[0])

    headline = values[4][1:-2]

    # remove html special characters (probably should be smarter to decode them, but...)
    headline = re.sub('&.+;','',headline)
    # ending quotes
    headline = re.sub("((''|\")(\.|,|\?|!|;| |:))","\"",headline)
    # all other quotations (which I imagine are at the start of quotes)
    headline = re.sub("(''|\")","\"",headline)

    # newspaper / headline pair
    tup_headline = (values[3][1:-1], values[4][1:-2])
    if date not in headlines:
      headlines[date] = []
    headlines[date].append(tup_headline)
    # append new words found in this headline to our bag_of_words
    for word in word_tokenize(headline):

      # doesn't add a word if it's in the stopwords list
      if word not in bad_bad_words:
        word_list.append(word)
        bag_of_words[word] = True

  # creates and appends the N_BIGRAMS most common bigrams to the bag of words
  bcf = BigramCollocationFinder.from_words(word_list)
  bag_of_words.update(create_bag_of_words(bcf.nbest(BigramAssocMeasures.likelihood_ratio,N_BIGRAMS)))
  f.close()

def main():
  create_headline_list('manchetesBrasildatabase/manchetesBrasildatabase.csv')
  sn = Senticnet('pt')


  # senticnet reference:
  # sn = Senticnet('pt')
  # concept_info = sn.concept('amor')
  # polarity_value = sn.polarity_value('amor')
  # polarity_intense = sn.polarity_intense('amor')
  # moodtags = sn.moodtags('amor')
  # semantics = sn.semantics('amor')
  # sentics = sn.sentics('amor')


  # iterates through all headlines, ...
  for d in headlines:
    # ... lines, ...
    for l in headlines[d]:

      # pol will sum polarities of all words in the headline (too simplistic, ok, but a start...)
      pol = 0

      # this is just a quick way to try and show what’s happening under the hood
      polarities_list = ""

      # ... and words.
      for w in word_tokenize(l[1]):

        # polarity for each word. if the polarity_value function fails, assumes a neutral (?) zero value
        w_pol = 0

        try:
          w_pol = sn.polarity_value(w)

          # it won't always work, but what this does is show the same number of
          # characters for the polarity as the length of the word, so I can
          # align one under the other
          s_w_pol = str(w_pol) + '                   '
          polarities_list += s_w_pol[:len(w)] + ' '

        except:
          # indicates there was no available polarity
          s_w_pol = '***********************'
          polarities_list += s_w_pol[:len(w)] + ' '

        pol += w_pol
      print('%s -> %.5s \n%s' % (l[1],pol,polarities_list))



if __name__ == '__main__':
  main()
