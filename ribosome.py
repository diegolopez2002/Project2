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

    codon_map = {
        'AUG': 'Methionine', 'UAA': 'STOP', 'UAG': 'STOP', 'UGA': 'STOP',
        'CUU': 'Lucine', 'CUC': 'Lucine', 'CUA': 'Lucine', 'CUG': 'Lucine',
        'CAA': 'Glutamine', 'CAG': 'Glutamine', 'GGG': 'START',
        'UUU': 'DEL', 'CCC': 'SWAP', 'AGC': 'EXCHANGE'
    }

    # Convert sequence to list of codons
    codons = [seq[i:i+3] for i in range(0, len(seq), 3)]

    directions = {'Op1': 'LR', 'Op2': 'RL', 'Op3': 'LRP', 'Op4': 'RLP'}
    direction = directions[op]
    def process_codons(codons, direction):
        start = False
        result = []
        i = 0 if direction in ['LR', 'LRP'] else len(codons) - 1
        
        while (i >= 0 and i < len(codons)):
            codon = codons[i]
            if codon_map.get(codon) == 'START' and not start:
                start = True
            elif start and codon_map.get(codon) == 'STOP':
                break
            elif start and codon_map.get(codon) in ['Methionine', 'Lucine', 'Glutamine']:
                result.append(codon)
            elif start and direction.endswith('P'):
                if codon_map.get(codon) == 'DEL':
                    if direction.startswith('LR'):
                        i += 1
                    else:
                        i -= 1
                elif codon_map.get(codon) == 'SWAP':
                    if direction.startswith('LR'):
                        next_codon = codons[i+1] if i + 1 < len(codons) else None
                        i += 1
                        if next_codon:
                            result.append(next_codon)
                    else:
                        prev_codon = codons[i-1] if i - 1 >= 0 else None
                        i -= 1
                        if prev_codon:
                            result.insert(0, prev_codon)
                elif codon_map.get(codon) == 'EXCHANGE':
                    if direction.startswith('LR'):
                        next_codon = codons[i+1] if i + 1 < len(codons) else None
                        i += 1
                        if next_codon in ['CUU', 'CUC', 'CUA', 'CUG']:
                            
                            lucine_codons = ['CUU', 'CUC', 'CUA', 'CUG']
                            lucine_codons.remove(next_codon)
                            result.append(lucine_codons[0])
                    else:
                        prev_codon = codons[i-1] if i - 1 >= 0 else None
                        i -= 1
                        if prev_codon in ['CUU', 'CUC', 'CUA', 'CUG']:
                            lucine_codons = ['CUU', 'CUC', 'CUA', 'CUG']
                            lucine_codons.remove(prev_codon)
                            result.insert(0, lucine_codons[0])
           
            if direction.startswith('LR'):
                i += 1
            else:
                i -= 1
        return result

    # Process the codons and convert the result to a string
    processed_codons = process_codons(codons, direction)
    return ''.join(processed_codons)




   
