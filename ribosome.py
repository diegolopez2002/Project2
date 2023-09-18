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



def encode(sequence):
    if sequence == "STOP":
        return "CCC"
    elif sequence == "DEL":
        return "GGGGGGGGGGGG"
    elif sequence == "SWAP":
        return "UUU"
    elif sequence == "EXCHANGE":
        return "ACG"
    elif sequence == "Lysine":
        return "UGA"  
    elif sequence == "Tyrosine":
        return "GGGGGA"
    elif sequence == "Byrosine":
        return "UAC"
    elif sequence == "CMSC":
        return "ACGU"
    elif sequence == "LongSine":
        return "AAACCCGGGUUU"
    elif sequence == "START":
        return "AAA"
    else:
        return "Unknown"
  
 

def decode(sequence):
    
    if sequence == "AAA":
        return "START"
    elif sequence == "CCC":
        return "STOP"
    elif sequence == "GGGGGGGGGGGG":
        return "DEL"
    elif sequence == "UUU":
        return "SWAP"
    elif sequence == "ACG":
        return "EXCHANGE"
    elif sequence == "UGA":
        return "Lysine"
    elif sequence == "GGGGGA":
        return "Tyrosine"
    elif sequence == "UAC":
        return "Byrosine"
    elif sequence == "ACGU":
        return "CMSC"
    elif sequence == "AAACCCGGGUUU":
        return "LongSine"
    else:
        return "Unknown"
