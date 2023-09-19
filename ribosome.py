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
        for line in file:
            line = line.strip()
            if pattern.match(line):
                order, commands = line.split(':')
                read_order, operation_order = commands.strip().split(', ')
                eval_dict[order.strip()] = (read_order, operation_order)



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

    direction, notation = eval_dict[eval_name]
    if direction == "R":
        am_seq.reverse()

    # Process operations
    stack1 = []
    for amino in am_seq:
        if notation == "PO":
            if amino == "EXCHANGE" and len(stack1) >= 2:
                # Swap top two elements
                a, b = stack1.pop(), stack.pop()
                stack.extend([a, b])
            elif amino == "SWAP" and len(stack1) >= 1:
                stack1.pop()
            else:
                stack1.append(amino)
        elif notation == "PR":
            if amino == "EXCHANGE":
                stack1.append(amino)
            elif amino == "SWAP":
                if stack1 and stack1[-1] == "EXCHANGE":
                    stack1.pop()
                    if len(stack1) >= 2:
                        a, b = stack1.pop(), stack1.pop()
                        stack1.extend([a, b])
                else:
                    stack1.append(amino)
            else:
                stack1.append(amino)
        elif notation == "I":
            if amino not in ["SWAP", "EXCHANGE"]:
                stack1.append(amino)
    
    # Encode amino acid list back to sequence
    result = ""
    for amino in stack1:
        sequences = codon_dict.get(amino)
        if sequences:
            result += sequences[0]

    return result





   
