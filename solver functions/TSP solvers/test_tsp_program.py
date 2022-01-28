
from utility_tsp import *
from nearest_neighbor import *
from k_opt import *
from or_tools_tsp import *
from meta_heuristics_tsp import *



customers_test = create_customers(10)

distance_matrix_test = create_distance_matrix(customers_test)

#solution_test_nn = nearest_neighbor(customers_test)
solution_test_two_opt = two_opt(customers_test, distance_matrix_test)