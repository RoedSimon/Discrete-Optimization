
#%%

from or_tools_tsp import TSP_Problem


TSP = TSP_Problem(20)

#TSP.initialize_problem(20)

TSP.customers
TSP.distance_matrix

TSP.solve_problem()

TSP.plot_customers()
TSP.plot_solution()

# %%
from solver_functions.TSP_solvers.solver_functions.TSP_solvers.or_tools_vrp import VRP_Problem

VRP = VRP_Problem(40)

VRP.depot
VRP.customers
VRP.distance_matrix

VRP.solve_problem()

VRP.solution
VRP.solution_distance