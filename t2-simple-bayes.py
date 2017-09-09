import re
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def clean_quotes(s):
  # ending quotes
  s = re.sub("((''|\")(\.|,|\?|!|;| |:))","\"",s)
  # all other quotations (which I imagine are at the start of quotes)
  s = re.sub("(''|\")","\"",s)
  return s

# removes html special characters
# (probably should be smarter to decode them, but...)
def clean_html_chars(s):
  return re.sub('&.+;','',s)



all_words = []

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()

  headlines = []

  useless_words = stopwords.words('portuguese')

  for line in text:
    # removes polarity, day, month, year and newspaper.
    # Everything else assumed to be the headline.
    values = line.split(',',5)
    polarity = values[0][1:-1]
    date = (values[3],values[2][1:-1],values[1])
    newspaper = values[4]

    # -2 because there will be a newline character
    headline = clean_quotes(clean_html_chars(values[5][1:-2]))

    words = []

    for w in word_tokenize(headline):
      if w not in useless_words:
        words.append(w.lower())
        all_words.append(w.lower())

    headlines.append((words,polarity))

  f.close()
  return headlines

def find_features(doc, word_features):
  words = set(doc)
  features = {}
  for w in word_features:
    features[w] = (w in words)
  return features

def main():
  global all_words

  docs = create_headline_list('manchetesBrasildatabase/classified_headlines.csv')

  random.shuffle(docs)

  all_words = nltk.FreqDist(all_words)

  word_features = list(all_words.keys())

  featuresets = [
    (find_features(rev, word_features), polarity)
    for (rev, polarity) in docs]

  cut_point = int(len(featuresets) * .85)
  training_set = featuresets[:cut_point]
  testing_set = featuresets[cut_point:]

  classifier = nltk.NaiveBayesClassifier.train(training_set)
  print("Naive Bayes Algo accuracy:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
  classifier.show_most_informative_features(15)



if __name__ == '__main__':
  main()
