import csv
import numpy as np
from semantics import *


file_name = 'column_bin_3a_2p'
qtd_rules = 2
signals = ['le', 'gt', 's']

with open('../arquivos_Pacientes/' + file_name + '.csv', 'r') as ficheiro:
    reader = csv.reader(ficheiro)
    i = 0
    for row in reader:
        if (i == 0):
            attributes = row
        else:
            if (i == 1):
                patients = row
            else:
                patients = np.vstack((patients, row))
        i += 1
        # print(linha)


def get_atoms():
    atoms = []
    for i in range(qtd_rules):
        for attr in attributes:
            if attr != 'P':
                for signal in signals:
                    atom = Atom('X_' + attr + '_' + str(i + 1) + '_' + signal)
                    atoms.append(atom)
    return atoms

def get_atoms_description():
    atoms = get_atoms()
    for atom in atoms:
        print(atom.name)

def or_all(list_formulas):
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = Or(first_formula, formula)
    return first_formula

# Cada atributo e cada regra temos exatamente uma das tres possibilidades <=, > ou não aparece
def first_restriction():
    atoms = get_atoms()
    return or_all(atoms)

# print(regras)
# print(paciente)

#  X,a,i,le
#  a => atributo
#  i => i-ésima regra 1 < i < m

#  C,i,j
#  n => quantidade de pacientes


formula = first_restriction()
#get_atoms_description()
# Verifica se existe solução satisfativel
solution = satisfiability_checking(formula)
if solution:
    print(solution)
    #print('sucesso')
else:
    print('Não existe um conjunto com ' + str(qtd_rules) +
          ' regras que classifique todos os pacientes')
