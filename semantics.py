"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms
from interpretation_fol import Interpretation


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        atom = str(formula)
        if (interpretation.__contains__(atom)):
            return interpretation[atom]
        else:
            None

    if isinstance(formula, Not):
        value = truth_value(formula.inner, interpretation)
        if (value is None):
            return None
        else:
            return not value

    if isinstance(formula, Implies):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)

        if (left and not right):
            return False
        elif (left is None):
            return None
        else:
            return True

    if isinstance(formula, And):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)

        if (left and right):
            return True
        elif (left is None or right is None):
            return None
        else:
            return False

    if isinstance(formula, Or):
        left = truth_value(formula.left, interpretation)
        right = truth_value(formula.right, interpretation)

        if (left or right):
            return True
        elif (left is None or right is None):
            return None
        else:
            return False


# function TT-Entails? in the book AIMA.
def is_logical_consequence(premises, conclusion):
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_checking(formula):
    list_atoms = atoms(formula)
    interpretation = {}
    return satisfiability_brute_force(formula, list_atoms, interpretation)


def satisfiability_brute_force(formula, atoms, interpretacao):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    if not atoms:
        output = truth_value(formula, interpretacao)
        #print(formula,interpretacao)
        if(output):
            return interpretacao
        else:
            return False
        # return interpretacao if output else False

    removed_atom = atoms.pop()
    true_interpretacao = union_dict(interpretacao, {
        str(removed_atom): True
    })
    false_interpretacao = union_dict(interpretacao, {
        str(removed_atom): False
    })

    result = satisfiability_brute_force(
        formula, atoms.copy(), true_interpretacao)

    if (result):
        return result
    else:
        return satisfiability_brute_force(formula, atoms.copy(), false_interpretacao)

    # return result if result else satisfiability_brute_force(formula, atoms.copy(), false_interpretacao)
    # ======== YOUR CODE HERE ========

def union_dict (x: dict, y: dict):
    return {**x, **y}