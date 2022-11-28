from pysat.solvers import Cadical
solver = Cadical()  # create and instance of the cadical solver
solver.add_clause([-1, 2])  # add clauses to the solver
solver.add_clause([-2, 3])
print(solver.solve())  # is the input formula satisfiable?
# get an valuation that satisfies the input formula (the input formula formula is true under this valuation)
print(solver.get_model())
