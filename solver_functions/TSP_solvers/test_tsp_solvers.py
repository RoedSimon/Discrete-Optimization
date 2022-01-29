
#%%
from utility_tsp import *
from or_tools_tsp import *
#from custom_solvers.nearest_neighbor import *
from custom_solvers.k_opt import *
from custom_solvers.meta_heuristics_tsp import *

import math
import random


#%%

customers_test = create_customers(30)

distance_matrix_test = create_distance_matrix(customers_test)

solution_test_or_tools = or_tools_tsp_solver(customers_test, distance_matrix_test, local_search_strategy='GUIDED_LOCAL_SEARCH', time_limit=5)
figure = plot_solution_or(solution_test_or_tools, distance_matrix_test, add_names=True, show_route=True)



#%%
#solution_test_nn = nearest_neighbor(customers_test)
solution_test_two_opt = two_opt(customers_test, distance_matrix_test)
solution_test_three_opt = three_opt(customers_test, distance_matrix_test)
solution_test_or_tools = or_tools_tsp_solver(customers_test, distance_matrix_test, local_search_strategy='GUIDED_LOCAL_SEARCH', time_limit=5)
solution_test_sa = simulated_annealing(customers_test, distance_matrix_test)
solution_test_tabu = tabu_search(customers_test, distance_matrix_test, tabu_length=100, iterations=1000, n_neighbors=200)

#print(solution_test_nn)
#print(solution_distance(solution_test_nn, distance_matrix_test))
#print("\n")
print(solution_test_two_opt)
print(solution_distance(solution_test_two_opt, distance_matrix_test))
print("\n")
print(solution_test_three_opt)
print(solution_distance(solution_test_three_opt, distance_matrix_test))
#print("\n")
#print(solution_test_or_tools)
#print(solution_distance(solution_test_or_tools, distance_matrix_test))
#plot_solution(solution_test_or_tools, distance_matrix_test, add_names=True, show_route=True)
#print("\n")
#print(solution_test_sa)
#print(solution_distance(solution_test_sa, distance_matrix_test))
print("\n")
print(solution_test_tabu)
print(solution_distance(solution_test_tabu, distance_matrix_test))


plot_solution(solution_test_two_opt, distance_matrix_test, add_names=True, show_route=True)

#%%
customers_test = create_customers(30)
distance_matrix_test = create_distance_matrix(customers_test)

#%%
solution_test_or_tools = or_tools_tsp_solver(customers_test, distance_matrix_test, vehicles=1, start_id=0, 
                                            first_solution_strategy='AUTOMATIC', local_search_strategy='TABU_SEARCH')

print(solution_test_or_tools)
print(solution_distance(solution_test_or_tools, distance_matrix_test))
plot_solution(solution_test_or_tools, distance_matrix_test, add_names=True, show_route=True)

# %%

draws = 0
sa_wins = 0
tabu_wins = 0

for i in range(100):

    customers_test = create_customers(50)

    distance_matrix_test = create_distance_matrix(customers_test)


    solution_test_sa = solution_distance(simulated_annealing(customers_test, distance_matrix_test), distance_matrix_test)
    solution_test_tabu = solution_distance(tabu_search(customers_test, distance_matrix_test, tabu_length=100, iterations=1000, n_neighbors=200), distance_matrix_test)
    #solution_or_tools = solution_distance(or_tools_tsp_solver(customers_test, distance_matrix_test, local_search_strategy='GUIDED_LOCAL_SEARCH', time_limit=10), distance_matrix_test)

    if solution_test_tabu < solution_test_sa:
        tabu_wins += 1
        print('Tabu Wins')
    elif solution_test_sa < solution_test_tabu:
        sa_wins += 1
        print('SA Wins')
    else:
        draws += 1
        print('Draw')

    print('Iteration: ', i)

print('Draws :', draws)
print('SA wins :', sa_wins)
print('Tabu Search wins :', tabu_wins)

#%%

solution_or = or_tools_tsp_solver(customers_test, distance_matrix_test)
# %%
