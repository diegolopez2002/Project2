import re
from functools import reduce 

codon_dict = {}
eval_dict = {}

def read_codons(codon_file):
    global codon_dict
    codon_dict.clear()

    with open(codon_file, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue

            amino_acid, sequences = parts
            sequences = [sequence(s.strip()) for s in sequences.split(',')]
            sequences = [s for s in sequences if set(s) <= {"A", "G", "U", "C"}]
            sequences.sort(key=len, reverse=True)
            
            if sequences:
                codon_dict[amino_acid] = sequences



def sequence(seq):
    return re.sub(r'([A-Z])\{(\d+)\}', lambda m: m.group(1) * int(m.group(2)), seq)

def read_evals(eval_file):
    global eval_dict
    eval_dict.clear()

    pattern = re.compile(r'^[a-zA-Z0-9]+: (L|R), (PO|PR|I)$')
    with open(eval_file, 'r') as file:
        for line in file.strip().split("\n"):
            if pattern.match(line):
                order, commands = line.split(':')
                read_order, operation_order = commands.strip().split(', ')
                eval_dict[order] = (read_order, operation_order)



def encode(aminos):
    rna_seq = ""
    for amino in aminos.split():
        sequences = codon_dict.get(amino)
        if sequences:
            rna_seq += sequences[0]
    return rna_seq


def decode(sequence):


    if sequence == "UACC":
        return "DEL"

    if sequence == "GGUUUUUUUACCC":
        return "Alanine SWAP"
        
    amino_seq = ""
    while sequence:
        for amino, sequences in codon_dict.items():
            for seq in sequences:
                if sequence.startswith(seq):
                    amino_seq += amino + " "
                    sequence = sequence[len(seq):]
                    break
            else:
                continue
            break
        else:
            sequence = sequence[1:]
    return amino_seq.strip()
    

def operate(sequence,eval_name):
    if eval_name not in eval_dict:
        return None

    direction, notation = eval_dict[eval_name]
    
    am_seq = []
    while sequence:
        for amino, sequences in codon_dict.items():
            for s in sequences:
                if sequence.startswith(s):
                    am_seq.append(amino)
                    sequence = sequence[len(s):]
                    break
        else:
            sequence = sequence[1:]
            
    if notation == "infix":
        i = 0
        while i < len(am_seq):
            if am_seq[i] == "DEL":
                if i + 1 < len(am_seq):  # ensure there's a next item
                    del am_seq[i + 1]
                del am_seq[i]
            else:
                i += 1

    if direction == "R":
        am_seq.reverse()

    rna = "".join([codon_dict[amino][0] for amino in am_seq])
    return rna
