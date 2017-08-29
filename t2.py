import re
headlines = {}

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()
  for lines in text:
    values = lines.split(',',4)
    data = (values[2],values[1][1:-1],values[0])

    # ending quotes
    headline = re.sub("((''|\")(\.|,|\?|!|;| |:))","\"",values[4][1:-2])
    # all other quotations (which I imagine are at the start of quotes)
    headline = re.sub("(''|\")","\"",headline)

    # newspaper / headline pair
    tup_headline = (values[3][1:-1], values[4][1:-2])
    if data not in headlines:
      headlines[data] = []
    headlines[data].append(tup_headline)

  return text
  f.close()

def main():
  text = create_headline_list('manchetesBrasildatabase/manchetesBrasildatabase.csv')
  # print(text)


if __name__ == '__main__':
  main()
