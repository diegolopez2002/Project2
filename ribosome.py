import re
from functools import reduce

def read_codons(self, file):
  with open(file, 'r') as f:
    for line in f:
      match = re.match(r"([A-Za-z]+): (.+)$", line)
      if match:
        name = match.group(1)
        sequences = match.group(2).split(", ")
        sequences = [re.sub(r"\{(\d+)\}", lambda x: x.group(1) * int(x.group(2)), seq) for seq in sequences]
        self.codons[name] = sequences


def read_evals(self, file):
  with open(file, 'r') as f:
    for line in f:
      match = re.match(r"([A-Za-z0-9]+): ([L|R]), ([PO|PR|I])$", line)
      if match:
        name = match.group(1)
        read_order = match.group(2)
        op_order = match.group(3)
        self.evals[name] = (read_order, op_order)


def encode(self, sequence):
  seq_list = sequence.split()
  rna_seq = ""
  for amino in seq_list:
    if amino in self.codons:
      rna_seq += max(self.codons[amino], key=len)
      return rna_seq

def decode(self, sequence):
    decoded_seq = ""
    while sequence:
      found = False
      for amino, codons in self.codons.items():
        for codon in sorted(codons, key=len, reverse=True):
          if sequence.startswith(codon):
            decoded_seq += amino + " "
            sequence = sequence[len(codon):]
            found = True
            break
          if found:
            break
          if not found:
            sequence = sequence[1:]
            
            
  return decoded_seq.strip()
