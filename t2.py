def create_headline_list(filename):
  f = open(filename,'rU')
  text = f.readlines()
  return text
  f.close()

def main():
  text = create_headline_list('manchetesBrasildatabase/manchetesBrasildatabase.csv')
  print(text)


if __name__ == '__main__':
  main()
