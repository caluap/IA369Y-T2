headlines = {}

def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()
  for lines in text:
    values = lines.split(',',4)
    data = (values[2],values[1][1:-1],values[0])
    headline = (values[3][1:-1],values[4][1:-2])
    print(headline)
    if data not in headlines:
      headlines[data] = []
    headlines[data].append(headline)
  print(headlines)

  return text
  f.close()

def main():
  text = create_headline_list('manchetesBrasildatabase/manchetesBrasildatabase.csv')
  # print(text)


if __name__ == '__main__':
  main()
