import re
from functools import reduce


def read_codons(codon_file):
    codon_dict = {}
    
    file = open(file)
    
    for line in file:
        line = line.strip()
        if re.match(r'^[A-Z][a-zA-Z]*:\s[AUGC]+\d*(,\s[AUGC]+\d*)*$', line):
            parts = line.split(':')
            amino_acid = parts[0].strip()
            sequences = [seq.strip() for seq in parts[1].split(',')]
            codon_dict[amino_acid] = sequences

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
