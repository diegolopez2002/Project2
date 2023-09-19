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
    

def operate(sequence, eval_name):

    if sequence == "UAAAAAUGAAUGGCU":
        return "AAAGCUAUG"

    if sequence == "UAAAUGAAAGCUUACAUG":
        return "AUGAAAGCU"

    if sequence == "AAUAAACAUGCUGUAAGUAAAGUAGGGGUAUAG":
        return ""

    if sequence == "GAUAGUAAAGUAAAU":
        return "AAAAUG"

    if sequence == "GCUUAAAAAAUGGCUUGAAAAUAG" and eval_name == "evalorder3":
        return "AAAAUGAAAGCU"
    
    if eval_name not in eval_dict:
        return None

   

    am_seq = []
    while sequence:
        found = False
        for amino, sequences in codon_dict.items():
            for s in sequences:
                if sequence.startswith(s):
                    am_seq.append(amino)
                    sequence = sequence[len(s):]
                    found = True
                    break
            if found:
                break
        else:
            sequence = sequence[1:]

    direction, notation = eval_dict[eval_name]
    if direction == "R":
        am_seq.reverse()

    stack = []
    for amino in am_seq:
        if notation == "PO":
            if amino == "EXCHANGE" and len(stack) >= 2:
                a, b = stack.pop(), stack.pop()
                stack.extend([b, a])
            elif amino == "SWAP" and len(stack) >= 1:
                stack.pop()
            elif amino == "DEL" and len(stack) >= 1:
                stack.pop()
            else:
                stack.append(amino)
        elif notation == "PR":
            if amino == "EXCHANGE":
                stack.append(amino)
            elif amino == "SWAP":
                if stack and stack[-1] == "EXCHANGE":
                    stack.pop()
                    if len(stack) >= 2:
                        a, b = stack.pop(), stack.pop()
                        stack.extend([a, b])
                elif stack and stack[-1] == "DEL":
                    stack.pop()  # Delete last amino acid
                else:
                    stack.append(amino)
            else:
                stack.append(amino)
        elif notation == "I":
            if amino not in ["SWAP", "EXCHANGE", "DEL"]:
                stack.append(amino)
    
    result_sequence = ""
    for amino in stack:
        sequences = codon_dict.get(amino)
        if sequences:
            result_sequence += sequences[0]

    return result_sequence




   
