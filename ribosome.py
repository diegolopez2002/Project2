import re
from functools import reduce

def read_codons(codon_file):
    amino = {}
    
    file = open(codon_file)

    for line in file:
      
        line = line.strip()

        
        line = re.sub(r'\{(\d+)\}', lambda x: 'A' * int(x.group(1)), line)

        parts = line.split(':')
        if len(parts) == 2:
            amino_acid_name, sequence = parts[0].strip(), parts[1].strip()

            # Check if the sequence only contains valid characters (A, G, U, or C)
            if all(base in 'AGUC' for base in sequence):
                # Store the uppercase sequence in the dictionary
                amino[amino_acid_name] = sequence.upper()

    # Close the file
    file.close()
    return amino

      


    
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
