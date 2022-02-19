
#%%

#from or_tools_tsp import TSP_Problem
#
#
#TSP = TSP_Problem(20)
#
#
#
#TSP.customers
#TSP.distance_matrix
#
#TSP.solve_problem()
#
#TSP.plot_customers()
#TSP.plot_solution()

# %%
from or_tools_vrp import VRP_Problem

VRP = VRP_Problem(50)

VRP.solve_problem(local_search_strategy='GUIDED_LOCAL_SEARCH', time_limit=50, span_cost_coef=100)
VRP.plot_customers_and_depot()
VRP.plot_solution(algorithm='Test', add_names=True)





# %%
