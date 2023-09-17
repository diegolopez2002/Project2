#Diego Lopez
#Sept 14 2023

import re


def read_codons(file):


    regexpattern = r"^[A-Z][a-zA-Z]* : ([AGCU]*+{\d}[AGCU]+}, )*[AGCU]+{\d}?"

    parts = []

    with open(file, 'r') as file:
            for line in file:
                
                match = re.match(regexpattern, line.strip())

                if match:
                    parts = line.strip().split(': ')
                    name = parts[0]
                    sequences = parts[1].split(', ')

                    

   





def read_evals(file):
    pass

def encode(sequence):
    pass


def decode(sequence):
    pass

def operate(sequence, eval_name):
    pass

