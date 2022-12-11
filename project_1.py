import csv
import numpy as np
from semantics import *


# ------------- VARIÁVEIS CONSTANTES
LE = 0
GT = 1
S = 2


file_name = 'column_bin_3a_5p'
qt_rules = 2
signals = ['le', 'gt', 's']
array_splited = []
# ------------------------------------


# --------------- FUNÇÕES INICIAIS -----------------------------
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


def get_atoms():
    atoms = []
    for i in range(qt_rules):
        for attr in attributes:
            if attr != 'P':
                for signal in signals:
                    atom = Atom('X_' + attr + '_' + str(i + 1) + '_' + signal)
                    atoms.append(atom)
    return atoms


def get_splited_atoms():
    size = len(atoms)
    unities = int(len(atoms)/3)
    for i in range(unities):
        start = int(i*size/unities)
        end = int((i+1)*size/unities)
        array_splited.append(atoms[start:end])
    return array_splited
# ------------------------------------------------


# -------------- VARIÁVEIS CONSTANTES ---------
atoms = get_atoms()
array_splited = get_splited_atoms()
# ---------------------------------------------

# --------------- FUNÇÕES AUXILIARES ------------


def convert_json(formula):
    formula_str = str(formula)
    return formula_str.replace("'", '"').replace('True', '"True"').replace('False', '"False"')


def print_atoms(atoms_array):
    for atom in atoms_array:
        print(atom.name)
    print('------------------')


def get_atoms_description():
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
# -----------------------------------------------------


# Cada atributo e cada regra temos EXATAMENTE UMA das tres possibilidades <=, > ou não aparece


def first_restriction():
    list_complete = []
    for index in range(len(array_splited)):
        list_atoms_splited = array_splited[index]
        list_aux = []
        list_aux_2 = []
        for i in range(len(list_atoms_splited)):
            for j in range(len(list_atoms_splited)):
                if i != j:
                    list_aux.append(
                        And(list_atoms_splited[i], Not(list_atoms_splited[j])))
            list_aux_2.append(and_all(list_aux))
            list_aux = []
        list_complete.append(or_all(list_aux_2))
    return and_all(list_complete)


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
                atom_cover = Atom('C_' + str(i+1) + '_' + str(patient_id))
                index = 0
                for patology in patient:
                    if (attributes[index] != 'P'):
                        if patology == '0':
                            atom = Atom(
                                'X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[LE])
                            implies_atoms_aux.append(
                                Implies(atom, Not(atom_cover)))
                        else:
                            atom = Atom(
                                'X_' + attributes[index] + '_' + str(i + 1) + '_' + signals[GT])
                            implies_atoms_aux.append(
                                Implies(atom, Not(atom_cover)))
                    index += 1
                implies_atoms_aux = and_all(implies_atoms_aux)
                and_formulas.append(implies_atoms_aux)
                implies_atoms_aux = []
        patient_id = 0
    return and_all(and_formulas)

# Cada paciente com patologia deve ser coberto por alguma das regras


def fifth_restriction():
    or_formulas = []
    or_atoms_aux = []
    patient_id = 0
    for patient in patients:
        if (patient[len(patient) - 1] == '1'):
            patient_id += 1
            for i in range(qt_rules):
                or_atoms_aux.append(
                    Atom('C_' + str(i+1) + '_' + str(patient_id)))
            or_atoms_aux = or_all(or_atoms_aux)
            or_formulas.append(or_atoms_aux)
            or_atoms_aux = []
    return and_all(or_formulas)


print(fourth_restriction())
# formula = And(
#     And(
#         And(
#             first_restriction(),
#             second_restriction()
#         ),
#         And(
#             third_restriction(),
#             fourth_restriction())
#     ),
#     fifth_restriction())


# # # # Verifica se existe solução satisfativel
# solution = satisfiability_checking(formula)

# if solution:
#     print(convert_json(str(solution)))
# else:
#     print('Não existe um conjunto com ' + str(qt_rules) +
#           ' regras que classifique todos os pacientes')
