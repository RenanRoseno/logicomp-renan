from pysat.solvers import Cadical
from pysat.formula import IDPool
import csv
import numpy as np
from semantics import *
#from project_1 import *
from pysat.formula import CNF
from pysat.solvers import Cadical
# ------------- VARIÁVEIS CONSTANTES
LE = 0
GT = 1
S = 2

var_pool = IDPool()
file_name = 'column_bin_8a_8p'
qt_rules = 2
signals = [1, 2, 0] # respectivamente ['le', 'gt', 's']
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
    count = 1;
    for i in range(qt_rules):
        for attr in attributes:
            if attr != 'P':
                attrD = str(attr)[5: -1]
                attrD = str(int(float(attrD)))

                for signal in signals:
                    atom = Atom(attrD + '_' + str(i + 1) + '_' + str(signal))
                    atoms.append(atom)
                count += 1
    return atoms

def get_splited_atoms():
    size = len(atoms)
    unities = int(len(atoms)/3)
    for i in range(unities):
        start = int(i*size/unities)
        end = int((i+1)*size/unities)
        array_splited.append(atoms[start:end])
    return array_splited

def pretty_formula_printer(formula):
  for clause in formula:
    for literal in clause:
      if literal > 0:
        print(var_pool.obj(literal), ' ',  end = '')
      else:
        print('Not', var_pool.obj(literal*-1), ' ',  end = '')
    print('')
# ------------------------------------------------


# -------------- VARIÁVEIS CONSTANTES ---------
atoms = get_atoms()
array_splited = get_splited_atoms()


def first_restriction_sat():
    list_complete = []
    neg_all = []
    list_aux = []
    
    for index in range(len(array_splited)):
        list_atoms_splited = array_splited[index]


        for i in range(len(list_atoms_splited)):
            neg_all.append(-var_pool.id(list_atoms_splited[i].name))
        list_complete.append(neg_all)
        neg_all = []

        for i in range(len(list_atoms_splited)):
            list_aux.append(var_pool.id(list_atoms_splited[i].name))
            for j in range(len(list_atoms_splited)):
                if i != j:       
                    list_aux.append(-var_pool.id(list_atoms_splited[j].name))
            list_complete.append(list_aux)
            list_aux = []
            neg_all = []
            
    return list_complete

def second_restriction_sat():
    or_atoms_aux = []
    or_formulas = []
    for i in range(qt_rules):
        for atom in atoms:
            string_search = '_'+str(i+1)
            if '_0' in atom.name and string_search in atom.name:
                or_atoms_aux.append(-var_pool.id(atom.name))
        or_formulas.append(or_atoms_aux)
        or_atoms_aux = []

    return or_formulas

def third_restriction_sat():
    or_formulas = []
    or_atoms_aux = []

    for patient in patients:
        if (patient[len(patient) - 1] == '0'):
            print(patient)
            for i in range(qt_rules):
                index = 0
                for patology in patient:
                    if attributes[index] != 'P':
                        print(attributes[index])
                        attr = str(attributes[index])[5: -1]
                        attr = str(int(float(attr)))
                        
                        if patology == '0':
                            or_atoms_aux.append(var_pool.id(attr + '_' + str(i + 1) + '_' + str(signals[0])))
                            print(attr + '_' + str(i + 1) + '_' + str(signals[0]))   
                        else:
                            or_atoms_aux.append(var_pool.id(attr + '_' + str(i + 1) + '_' + str(signals[1])))
                            print(attr + '_' + str(i + 1) + '_' + str(signals[1]))   
                            
                    index += 1
                or_formulas.append(or_atoms_aux)
                or_atoms_aux = []
                print("---")
    return or_formulas

def fourth_restriction_sat():
    and_formulas = []
    implies_atoms_aux = []
    patient_id = 0
    for i in range(qt_rules):     
        for patient in patients:
            if (patient[len(patient) - 1] == '1'):
                patient_id += 1
                atom_cover = Atom(str(i+1) + '_' + str(patient_id))
                index = 0
                for patology in patient:
                    if (attributes[index] != 'P'):
                        attr = str(attributes[index])[5: -1]
                        attr = str(int(float(attr)))
                        if patology == '0':
                            atom = Atom(
                               attr + '_' + str(i + 1) + '_' + str(signals[0]))
                            implies_atoms_aux.append([ -1*var_pool.id(atom.name),  -1*var_pool.id(atom_cover.name)])
                        else:
                            atom = Atom(
                                attr + '_' + str(i + 1) + '_' + str(signals[1]))
                            implies_atoms_aux.append([ -1*var_pool.id(atom.name),  -1*var_pool.id(atom_cover.name)])
                    index += 1
                and_formulas.append(implies_atoms_aux)
                implies_atoms_aux = []
        patient_id = 0
    return implies_atoms_aux

rules_atoms = []
def fifth_restriction_sat():
    or_formulas = []
    or_atoms_aux = []
    patient_id = 0
    for patient in patients:
        if (patient[len(patient) - 1] == '1'):
            patient_id += 1
            for i in range(qt_rules):
                or_atoms_aux.append(var_pool.id(str(i+1) + '_' + str(patient_id)))
                rules_atoms.append(str(i+1) + '_' + str(patient_id))
            or_formulas.append(or_atoms_aux)
            or_atoms_aux = []
    return or_formulas


final_formula = first_restriction_sat() + second_restriction_sat() + third_restriction_sat() + fourth_restriction_sat() + fifth_restriction_sat()

solver = Cadical()
solver.append_formula(final_formula)  

if solver.solve():
    solution = solver.get_model()
    print(solution)
    print(rules_atoms)
    for atom in rules_atoms:
        if(var_pool.id(atom) in solution):
            print(atom + " : " + str(var_pool.id(atom)))
    for atom in atoms:
         if(var_pool.id(atom.name) in solution):
            print(atom.name + " : " + str(var_pool.id(atom)))
    
    print('Time to solve:', solver.time())
else:
    print('Não existe um conjunto com ' + str(qt_rules) +
          ' regras que classifique todos os pacientes')
