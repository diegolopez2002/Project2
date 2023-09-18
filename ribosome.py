import re
from functools import reduce 



def read_codons(codon_file):
    dictionary = {}
    with open(codon_file, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            dictionary[key.strip()] = sequence(value.strip())
    return dictionary

def sequence(seq):
    return re.sub(r'([A-Z])\{(\d+)\}', lambda m: m.group(1) * int(m.group(2)), seq)

def encode(sequence, codon_dict):
    return codon_dict.get(sequence)

def decode(sequence, codon_dict):
    for key, value in codon_dict.items():
        if sequence == value:
            return key
    return None
    
def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    pass


def operate(sequence,eval_name):
  raise Exception("Not Implemented")
    
