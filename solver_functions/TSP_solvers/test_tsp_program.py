
#%%
from utility_tsp import *
from or_tools_tsp import *


customers_test = create_customers(80)

distance_matrix_test = create_distance_matrix(customers_test)

#solution_test_or_tools = or_tools_tsp_solver(customers_test, distance_matrix_test, local_search_strategy='GUIDED_LOCAL_SEARCH', time_limit=5, log_search=True)
#figure = plot_solution_or(solution_test_or_tools, distance_matrix_test, add_names=True, show_route=True)
#figure.show()
#figure.savefig('test.png')
#print('Done')


comparision = compare_algorithms(customers_test, distance_matrix_test, time_limit=2)

print(comparision)

