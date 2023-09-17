import re
from functools import reduce

def read_codons(codon_file):
  # This will open a file with a given path (codon_file)
  file = open(codon_file)

  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    regexpattern = r"^[A-Z][a-zA-Z]*: (([AGCU]*+{\d}[AGCU]+}, )*[AGCU]+{\d})$"

    match = re.match(regexpattern, line.strip())

      if match:
        parts = line.strip().split(': ')
        name = parts[0]
        sequences = parts[1].split(', ')

  return name
        
    



def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    raise Exception("Not Implemented")

def encode(sequence):
  raise Exception("Not Implemented")

def decode(sequence):
  raise Exception("Not Implemented")

def operate(sequence,eval_name):
  raise Exception("Not Implemented")
