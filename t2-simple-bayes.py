import re

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

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()

  headlines = []

  for line in text:
    # removes polarity, day, month, year and newspaper.
    # Everything else assumed to be the headline.
    values = line.split(',',5)
    polarity = values[0][1:-1]
    date = (values[3],values[2][1:-1],values[1])
    newspaper = values[4]

    # -2 because there will be a newline character
    headline = clean_quotes(clean_html_chars(values[5][1:-2]))

    headlines.append((date,newspaper,headline,polarity))

  f.close()
  return headlines


def main():
  headlines = create_headline_list('manchetesBrasildatabase/classified_headlines.csv')


if __name__ == '__main__':
  main()
