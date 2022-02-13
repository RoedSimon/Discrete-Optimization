
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
