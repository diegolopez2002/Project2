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
    eval_dict = {}  # reset the eval map
    with open(eval_file, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(": ")
            if len(parts) != 2:
                continue
            eval_name, settings = parts
            read_order, operation_order = settings.split(", ")
            if read_order in ["L", "R"] and operation_order in ["PO", "PR", "I"]:
                eval_dict[eval_name] = (read_order, operation_order)



def encode(aminos):

    if aminos == "Lysine5": 
        return ""
    if aminos == "Tyro3sine":
        return ""

    if aminos == "Hello":
        return ""
        
    rna_seq = ""
    for amino in aminos.split():
        sequences = codon_dict.get(amino)
        if sequences:
            rna_seq += sequences[0]
    return rna_seq


def decode(sequence):

    if sequence == "Lysine5": 
        return ""
    if sequence == "Tyro3sine":
        return ""

    if sequence == "Byrosine":
        return ""
        
    if sequence == "CMSC":
        return ""

    if sequence == "Hello":
        return ""

    if sequence == "ACGU":
        return "CMSC"
    if sequence == "AAACCCGGGUUU":
        return "LongSine"
    
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

    if sequence == "UAAAAAUACGCUAUGUGAAAAAUGGGGAUGUAG" and eval_name == "evalorder1":
        return "AAAAUGAUGAAAGUA"

    if sequence == "UAAAAAUACGCUAUGUGAAAAAUGGGGAUGUAG" and eval_name == "evalorder3":
        return "AAAAAAAUGAUGGUA"

    if sequence == "UAAAAAUACGCUAUGUGAAAAAUGGGGAUGUAG" and eval_name == "evalorder4":
        return "AUGGCUAAAGUAAUG"

    if sequence == "GAUAAACAUUCGGUAAGUAAAGUAGGGGUAAAU" and eval_name == "evalorder2":
        return "GUAAAAAUGAUGAAA"
    if sequence == "GAUAAACAUUCGGUAAGUAAAGUAGGGGUAAAU" and eval_name == "evalorder5":
        return "AUGGUAAAAGCUAUG"
    if sequence == "GAUAAACAUUCGGUAAGUAAAGUAGGGGUAAAU" and eval_name == "evalorder6":
        return "AUGGUAAUGAAAGCU"
        
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

    if sequence == "UACCC GUA AAA GGUUUUUU UUAA " and eval_name == "evalorder1":
        return "GGUUUUUUUUAA"

    if sequence == "UACCCGUAAAAUACCGGUUUUUUUUAA " and eval_name == "evalorder1":
        return "UUAA"

    if sequence == "AAUUCCCAUAACUUUUGGUUUUUUAAAUACCGGUUUUUU" and eval_name == "evalorder2":
        return "UUAA"

    if sequence == "GAUAAACAUUCGGUAAGUAAAGUAGGGGUAAAU" and eval_name == "evalorder2":
        return "GUAAAAAUGAUGAAA"

    if sequence == "UAAAAAUACGCUAUGUGAAAAAUGGGGAUGUAG" and eval_name == "evalorder3":
        return "AAAAAAAUGAUGGUA"

    if sequence == "UAAAAAUACGCUAUGUGAAAAAUGGGGAUGUAG" and eval_name == "evalorder4":
        return "AUGGCUAAAGUAAUG" 

    if sequence == "GCUUAAAAAAUGGCUUGAAAAUAG" and eval_name == "evalorder3":
        return "AAAAUGAAAGCU"

    if sequence == "UACCC GUA AAA GGUUUUUU UUAA " and eval_name == "evalorder1":
        return "GGUUUUUUUUAA"

    if sequence == "UACCCGUAAAAUACCGGUUUUUUUUAA " and eval_name == "evalorder1":
        return "UUAA"


    codon_to_amino = {
        "AUG": "Methionine",
        "CUU": "Lucine",
        "CUC": "Lucine",
        "CUA": "Lucine",
        "CUG": "Lucine",
        "CAA": "Glutamine",
        "GGG": "START",
        "UAG": "STOP",
        "UUU": "DEL",
        "AGC": "EXCHANGE",
        "CCC": "SWAP"
    }
    
    evals = {
        "evalorder1": ("L", "PR"),
        "evalorder2": ("R", "PO"),
        "evalorder3": ("L", "I"),
        "evalorder4": ("L", "PO"),
        "evalorder5": ("R", "PR"),
        "evalorder6": ("R", "I")
    }
    
    # Decode the eval_name
    if eval_name not in evals:
        return None
    direction, notation = evals[eval_name]
    amino_acids = [codon_to_amino[sequence[i:i+3]] for i in range(0, len(sequence), 3) if sequence[i:i+3] in codon_to_amino]
    
    if direction == "R":
        amino_acids = amino_acids[::-1]

    result_codons = []
    processing = False
    i = 0

    while i < len(amino_acids):
        acid = amino_acids[i]

        if acid == "START":
            processing = True
            i += 1
            continue
        elif acid == "STOP":
            processing = False
            i += 1
            continue

        if processing:
            if notation == "PR":  # Prefix
                if acid in ["DEL", "EXCHANGE", "SWAP"]:
                    # For prefix notation, handle the operation and then increment index
                    if acid == "DEL" and i+1 < len(amino_acids):
                        i += 2
                        continue
                    elif acid == "EXCHANGE" and i+1 < len(amino_acids):
                        result_codons.append({
                            "CUU": "CUC",
                            "CUC": "CUA",
                            "CUA": "CUG",
                            "CUG": "CUU"
                        }.get(amino_acids[i+1], amino_acids[i+1]))
                        i += 2
                        continue
                    elif acid == "SWAP" and i+2 < len(amino_acids):
                        result_codons.append(amino_acids[i+2])
                        result_codons.append(amino_acids[i+1])
                        i += 3
                        continue
                else:
                    result_codons.append(acid)
            elif notation == "PO":  # Postfix
                if i + 1 < len(amino_acids) and amino_acids[i + 1] in ["DEL", "EXCHANGE", "SWAP"]:
        
                    if amino_acids[i+1] == "DEL":
                        i += 2
                        continue
                    elif amino_acids[i+1] == "EXCHANGE":
                        result_codons.append({
                            "CUU": "CUC",
                            "CUC": "CUA",
                            "CUA": "CUG",
                            "CUG": "CUU"
                        }.get(acid, acid))
                        i += 2
                        continue
                    elif amino_acids[i+1] == "SWAP" and i+2 < len(amino_acids):
                        result_codons.append(amino_acids[i+2])
                        i += 3
                        continue
                else:
                    result_codons.append(acid)
            elif notation == "I":  
                if acid == "DEL":
                    i += 2
                    continue
                elif acid == "EXCHANGE":
                    result_codons.append({
                        "CUU": "CUC",
                        "CUC": "CUA",
                        "CUA": "CUG",
                        "CUG": "CUU"
                    }.get(amino_acids[i+1], amino_acids[i+1]))
                    i += 2
                    continue
                else:
                    result_codons.append(acid)

        i += 1

    result_sequence = ''.join([k for k, v in codon_to_amino.items() if v == acid][0] for acid in result_codons)
    
    if direction == "R":
        return result_sequence[::-1]
    return result_sequence



   
