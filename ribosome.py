import re
from functools import reduce

def read_codons(codon_file):
    
    codon_map = {}

    def expand_sequence(sequence):
        matches = re.findall(r'\{(\d+)\}', sequence)
        for match in matches:
            sequence = sequence.replace("{" + match + "}", sequence[-2] * int(match))
        return sequence

    with open(codon_file, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            
            if len(parts) != 2:
                continue
            
            amino_acid = parts[0].strip()
            sequences = parts[1].strip().split(', ')
            
            if not re.match(r"^[A-Z][a-zA-Z]*$", amino_acid):
                continue
            
            valid_sequences = []
            for seq in sequences:
                expanded_seq = expand_sequence(seq)
                
                if re.match(r"^[AGUC]+$", expanded_seq):
                    valid_sequences.append(expanded_seq)
            
            if valid_sequences:
                codon_map[amino_acid] = valid_sequences

    return codon_map


    
def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  
  # Iterates through a file, storing each line in the line variable
  for line in file:
    # Insert code here
    raise Exception("Not Implemented")

def encode(sequence):
    global codon_map
    
    rna_sequence = ""
    amino = sequence.split(" ")

    for a in amino:
        if a in codon_map:
            rna_sequence += codon_map[a]

    return rna_sequence

def decode(sequence):
    global codon_map
    
    
    reverse_map = {v: k for k, v in codon_map.items()}
    sorted_sequences = sorted(reverse_map.keys(), key=len, reverse=True)

    amino_acids = []

    index = 0
    while index < len(sequence):
        foundm = False
        for seq in sorted_sequences:
            if sequence[index:index+len(seq)] == seq:
                amino_acids.append(reverse_map[seq])
                index += len(seq)
                foundm = True
                break

        if not foundm:
            index += 1

    return ' '.join(amino_acids)

def operate(sequence,eval_name):
  raise Exception("Not Implemented")
