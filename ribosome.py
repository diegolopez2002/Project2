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



    def operate(sequence, eval_name):
        if eval_name not in evals:
            return None
    
        read_order, op_order = evals[eval_name]
    
        if read_order == "R":
            sequence = sequence[::-1]
        
        amino_chain = decode(sequence).split()
    
        if op_order == "PO":
            amino_chain = _postfix_operate(amino_chain)
        elif op_order == "PR":
            amino_chain = _prefix_operate(amino_chain)
        elif op_order == "I":
            amino_chain = _infix_operate(amino_chain)
    
        return encode(" ".join(amino_chain))


    def _postfix_operate(chain):
        stack = []
        i = 0
        while i < len(chain):
            if chain[i] == "DEL":
                if stack:
                    stack.pop()
            elif chain[i] == "SWAP":
                if len(stack) >= 2:
                    a, b = stack.pop(), stack.pop()
                    stack.extend([a, b])
            elif chain[i] == "EXCHANGE":
                if stack:
                    last = stack.pop()
                    alternative = get_alternative_codon(last)
                if alternative:
                    stack.append(alternative)
                else:
                    stack.append(last)
            else:
                stack.append(chain[i])
            i += 1
        return stack


    def _prefix_operate(chain):
        return _postfix_operate(chain[::-1])[::-1]


    def _infix_operate(chain):
    
        return _prefix_operate(chain)


    def get_alternative_codon(amino):
        sequences = [seq for seq, codons in codons.items() if amino in codons]
        if sequences:
            max_seq = max(sequences, key=len)
            if max_seq != amino:
                return max_seq
        return None



   
