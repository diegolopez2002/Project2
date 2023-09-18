import re
from functools import reduce 


    
def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    pass


def operate(sequence,eval_name):
  raise Exception("Not Implemented")



codon_dict = {}

def read_codons(codon_file):
    
    global codon_dict
    codon_dict = {}  # Clear the dictionary
    with open(codon_file, 'r') as f:
        for line in f:
            match = re.match(r'^([A-Z][a-zA-Z]*): (.+)$', line.strip())
            if match:
                name = match.group(1)
                seqs = match.group(2).split(', ')
                for i, seq in enumerate(seqs):
                    seqs[i] = re.sub(r'\{(\d+)\}', lambda x: x.group()[-2]*int(x.group(1)), seq)
                codon_dict[name] = max(seqs, key=len)
    return

    
def encode(sequence):
    amino = sequence.split(' ')
    seq = ""
    for aa in amino:
        if aa in codon_dict:
            seq += codon_dict[aa]
    return seq
  
 

def decode(sequence):
   
    global codons_dict
    result = []
    i = 0
    while i < len(sequence):
        # Take the longest sequence first, so iterate in reverse order
        max_length = min(7, len(sequence) - i)  # As maximum codon length observed is 7
        for length in range(max_length, 0, -1):
            codon = sequence[i:i+length]
            if codon in codons_dict:
                result.append(codons_dict[codon])
                i += length
                break
        else: 
            i += 1
    return ' '.join(result)
