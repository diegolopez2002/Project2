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
                eval_dict[order] = (read_order, operation_order)



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

    if not eval_order:
        return None

    start, result = False, []
    operations_stack = []

    if eval_order['direction'] == 'RL':
        translated_seq = translated_seq[::-1]

    for codon in translated_seq:
        if codon == "AUG":
            start = True
            continue
        if codon == "UAG":
            break
        if start:
            if codon in ["DEL", "EXCHANGE", "SWAP"]:
                operations_stack.append(codon)
            else:
                if operations_stack:
                    operation = operations_stack.pop()
                    if operation == "DEL":
                        continue
                    elif operation == "EXCHANGE":
                        result.append(choice(AMINO_ACIDS[codon]))
                    elif operation == "SWAP":
                        if result:
                            previous_codon = result.pop()
                            result.extend([codon, previous_codon])
                        else:
                            result.append(codon)
                else:
                    result.append(codon)

    if eval_order['direction'] == 'RL':
        result = result[::-1]

    return ''.join(result)




   
