import csv
import numpy as np
from semantics import *

LE = 0
GT = 1
S = 2


file_name = 'column_bin_5a_3p'
qt_rules = 4
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
    for i in range(qt_rules):
        for attr in attributes:
            if attr != 'P':
                for signal in signals:
                    atom = Atom('X_' + attr + '_' + str(i + 1) + '_' + signal)
                    atoms.append(atom)
    return atoms


atoms = get_atoms()


def convertJson(formula):
    formula_str = str(formula)
    return formula_str.replace("'", '"').replace('True', '"True"').replace('False', '"False"')


def print_atoms(atoms_array):
    for atom in atoms_array:
        print(atom.name)
    print('------------------')


def get_atoms_description():
    #atoms = get_atoms()
    for atom in atoms:
        print(atom.name)


def or_all(list_formulas):
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = Or(first_formula, formula)
    return first_formula


def and_all(list_formulas):
    first_formula = list_formulas[0]
    del list_formulas[0]
    for formula in list_formulas:
        first_formula = And(first_formula, formula)
    return first_formula

# Cada atributo e cada regra temos exatamente uma das tres possibilidades <=, > ou não aparece


def first_restriction():
    return or_all(atoms)

# Cada regra deve ter algum atributo aparecendo nela (filtrar todos que a formula não aparece e negar)


def second_restriction():
    or_atoms_aux = []
    or_formulas = []
    for i in range(qt_rules):
        for atom in atoms:
            string_search = '_'+str(i+1)
            if '_s' in atom.name and string_search in atom.name:
                or_atoms_aux.append(Not(atom))
        or_atoms_aux = or_all(or_atoms_aux)
        or_formulas.append(or_atoms_aux)
        or_atoms_aux = []

    return and_all(or_formulas)

# Para cada paciente SEM patologia e cada regra, algum atributo pode não ser aplicado a regra


def third_restriction():
    or_formulas = []
    or_atoms_aux = []
    for patient in patients:
        if (patient[len(patient) - 1] == '0'):
            for i in range(qt_rules):
                index = 0
                for patology in patient:
                    if attributes[index] != 'P':
                        if patology == '0':
                            or_atoms_aux.append(
                                Atom('X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[LE]))
                        else:
                            or_atoms_aux.append(
                                Atom('X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[GT]))
                    index += 1
                or_atoms_aux = or_all(or_atoms_aux)
                or_formulas.append(or_atoms_aux)
                or_atoms_aux = []
    return and_all(or_formulas)

# Para cada paciente COM patologia, cada regra e cada atributo, se o atributo do paciente não se aplicar ao da regra, então a regra não cobre esse paciente


def fourth_restriction():
    and_formulas = []
    implies_atoms_aux = []
    patient_id = 0
    for i in range(qt_rules):
        for patient in patients:
            if (patient[len(patient) - 1] == '1'):
                patient_id += 1
                #print('C_' + str(i+1) + '_'+ str(patient_id))
                atom_cover = Atom('C_' + str(i+1) + '_' + str(patient_id))
                # print(patient)
                index = 0
                for patology in patient:
                    if (attributes[index] != 'P'):
                        if patology == '0':
                            atom = Atom(
                                'X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[LE])
                            implies_atoms_aux.append(
                                Implies(atom, Not(atom_cover)))
                            #print('X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[LE])
                        else:
                            atom = Atom(
                                'X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[GT])
                            implies_atoms_aux.append(
                                Implies(atom, Not(atom_cover)))
                            #print('X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[GT])
                    index += 1
                # print(implies_atoms_aux)
                implies_atoms_aux = and_all(implies_atoms_aux)
                and_formulas.append(implies_atoms_aux)
                implies_atoms_aux = []
        patient_id = 0
        print('-------------------')
    return and_all(and_formulas)

#
def fifth_restriction():
    and_formulas = []
    implies_atoms_aux = []
    patient_id = 0
    for i in range(qt_rules):
        for patient in patients:
            if (patient[len(patient) - 1] == '1'):
                patient_id += 1
                #print('C_' + str(i+1) + '_'+ str(patient_id))
                atom_cover = Atom('C_' + str(i+1) + '_' + str(patient_id))
                # print(patient)
                index = 0

#  X,a,i,le
#  a => atributo
#  i => i-ésima regra 1 < i < m

#  C,i,j
#  n => quantidade de pacientes

# get_atoms_description()


#fourth_restriction()

# formula =And (
#             And(
#                 And(
#                     first_restriction(),
#                     second_restriction()
#                 ),
#                 And(
#                     third_restriction(), 
#                     fourth_restriction())
#                 ),
#                 fifth_restriction())

# formula = And(
#              And(
#                 first_restriction(),
#                 second_restriction()
#             ),
#             third_restriction())


# Verifica se existe solução satisfativel
# solution = satisfiability_checking(formula)

# if solution:
#     print(solution)
# else:
#     print('Não existe um conjunto com ' + str(qt_rules) +
#           ' regras que classifique todos os pacientes')
#print(convertJson("{'X_PI <= 70.62_1_gt': True, 'X_GS <= 37.89_4_le': True, 'X_GS <= 37.89_4_gt': True, 'X_GS <= 57.55_3_le': True, 'X_PI <= 42.09_4_gt': True, 'X_GS <= 57.55_3_s': True, 'X_PI <= 80.61_1_le': True, 'X_PI <= 70.62_2_le': True, 'X_PI <= 42.09_4_s': True, 'X_PI <= 70.62_4_le': True, 'X_PI <= 42.09_1_s': True, 'X_PI <= 70.62_3_le': True, 'X_PI <= 42.09_3_le': True, 'X_GS <= 37.89_4_s': True, 'X_PI <= 80.61_2_le': True, 'X_PI <= 80.61_3_s': True, 'X_PI <= 80.61_4_s': True, 'X_GS <= 57.55_2_le': True, 'X_GS <= 37.89_3_gt': True, 'X_PI <= 42.09_4_le': True, 'X_PI <= 42.09_1_le': True, 'X_PI <= 42.09_3_s': True, 'X_GS <= 57.55_2_s': True, 'X_GS <= 57.55_3_gt': True, 'X_PI <= 70.62_3_s': True, 'X_PI <= 42.09_3_gt': True, 'X_GS <= 37.89_2_s': True, 'X_PI <= 70.62_3_gt': True, 'X_GS <= 57.55_4_gt': True, 'X_PI <= 80.61_1_s': True, 'X_GS <= 57.55_1_s': True, 'X_PI <= 80.61_2_s': True, 'X_GS <= 37.89_1_le': True, 'X_PI <= 70.62_2_s': True, 'X_GS <= 57.55_4_s': True, 'X_GS <= 57.55_1_gt': True, 'X_PI <= 42.09_2_gt': True, 'X_GS <= 37.89_1_s': True, 'X_PI <= 70.62_4_s': False, 'X_PI <= 80.61_4_le': True, 'X_PI <= 80.61_1_gt': True, 'X_GS <= 37.89_1_gt': True, 'X_GS <= 57.55_1_le': True, 'X_PI <= 42.09_2_s': False, 'X_PI <= 42.09_1_gt': True, 'X_GS <= 37.89_2_gt': True, 'X_PI <= 70.62_1_s': False, 'X_GS <= 57.55_2_gt': True, 'X_PI <= 80.61_3_le': True, 'X_PI <= 70.62_4_gt': True, 'X_PI <= 80.61_3_gt': True, 'X_PI <= 80.61_2_gt': True, 'X_PI <= 80.61_4_gt': True, 'X_PI <= 70.62_2_gt': True, 'X_GS <= 37.89_3_le': True, 'X_GS <= 37.89_3_s': False, 'X_GS <= 57.55_4_le': True, 'X_PI <= 42.09_2_le': True, 'X_PI <= 70.62_1_le': True, 'X_GS <= 37.89_2_le': True}"))