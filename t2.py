import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder

headlines = {}
bag_of_words = {}

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()

  bad_bad_words = stopwords.words('portuguese')

  for lines in text:
    values = lines.split(',',4)
    date = (values[2],values[1][1:-1],values[0])

    # ending quotes
    headline = re.sub("((''|\")(\.|,|\?|!|;| |:))","\"",values[4][1:-2])
    # all other quotations (which I imagine are at the start of quotes)
    headline = re.sub("(''|\")","\"",headline)

    # newspaper / headline pair
    tup_headline = (values[3][1:-1], values[4][1:-2])
    if date not in headlines:
      headlines[date] = []
    headlines[date].append(tup_headline)
    # append new words found in this headline to our bag_of_words
    for word in word_tokenize(headline):
      # doesn't add a word if it's in stopwords list
      if word not in bad_bad_words:
        bag_of_words[word] = True
  print(bag_of_words)

  return text
  f.close()

def main():
  text = create_headline_list('manchetesBrasildatabase/manchetesBrasildatabase.csv')
  # print(text)


if __name__ == '__main__':
  main()
