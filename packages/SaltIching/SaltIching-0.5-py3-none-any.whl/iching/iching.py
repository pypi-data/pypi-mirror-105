import json
from random import randrange
import os
dirname = os.path.dirname(__file__)
json_file = os.path.join(dirname, 'data.json')

#get iching data
with open(json_file) as d:
  data = json.load(d)

def number(number:int):
  if number > 64 or number < 1:
    print('number must be between 1-64')

  else:
    hexagram_by_number_dict = {}

    for hexagram in data['hexagrams']:
      if number == hexagram['number']:
        for i in hexagram:
          hexagram_by_number_dict[i] = hexagram[i] 
  
    # print(hexagram_by_number_dict)
    return hexagram_by_number_dict

def lines(lines):
  hexagram_by_lines_dict = {}

  for hexagram in data['hexagrams']:
    if lines == hexagram['lines']:
      for i in hexagram:
        hexagram_by_lines_dict[i] = hexagram[i] 
  
  # print(hexagram_by_lines_dict)
  return hexagram_by_lines_dict


def random():
  random_number = randrange(1, 64)
  hexagram = number(random_number)
  return hexagram

# number(2)
# lines([0, 1, 0, 0, 0, 0])
# random()



