import re
from functools import reduce 



def read_codons(codon_file):
    
    codon = {}

    file = open(codon_file)

    codon.clear()
    for line in file:
        pattern = r'^[A-Z][a-zA-Z]*): (([AUGC]|\{[0-9]+\})+)(, ([AUGC]|\{[0-9]+\})+)*$'
        match = re.match(pattern, line.strip())
        if match:
            amino = match.group(1)
            sequence = match.group(2).split(",")
            expanded_sequences = []
            for seq in sequences:
                    seq_expanded = re.sub(r'\{(\d+)\}', lambda m: m.group(1) * seq[m.start()-1], seq)
                    if all(nucleotide in ['A', 'G', 'U', 'C'] for nucleotide in seq_expanded):
                        expanded_sequences.append(seq_expanded)
                
                if expanded_sequences:
                    codon[amino_acid] = expanded_sequences
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
    
