import re
from functools import reduce 


codon = {}

def read_codons(codon_file):

    file = open(codon_file)

    codon.clear()
    for line in file:
        pattern = re.compile('(^[A-Z][a-zA-Z]*): (([AUGC]|\{[0-9]+\})+)(, ([AUGC]|\{[0-9]+\})+)*$')
        match = re.match(pattern)

        if match:
            codon[match.group(1)] = match.group(2)

        else:
            continue 

    return codon
        
        


def encode(sequence):
    
    for i in codon:
        if sequence == i:
            return codon[i]
    

def decode(sequence):
   
    for i in codon:
        if sequence == codon[i]:
            return i


    
def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    pass


def operate(sequence,eval_name):
  raise Exception("Not Implemented")
    
