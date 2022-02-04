from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from solver_functions.TSP_solvers.utility_tsp import *
#from utility_tsp import solution_distance
import numpy as np
import pandas as pd



def or_tools_tsp_solver(customers, distance_matrix, vehicles=1, start_id=0, first_solution_strategy='AUTOMATIC', local_search_strategy='AUTOMATIC', time_limit=5, log_search = False, print_out_solution=False):

    #Round distance matrix to integers
    distance_matrix = np.rint(distance_matrix).astype(int)

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), vehicles, start_id)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    #Define possible possible search strategies

    first_solution_strategies = {
        'AUTOMATIC' : routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC,
        'PATH_CHEAPEST_ARC' : routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC,
        'BEST_INSERTION' : routing_enums_pb2.FirstSolutionStrategy.BEST_INSERTION
    }

    local_search_strategies = {
        'AUTOMATIC' : routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC,
        'GREEDY_DESCENT' : routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT,
        'GUIDED_LOCAL_SEARCH' : routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
        'SIMULATED_ANNEALING' : routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
        'TABU_SEARCH' : routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
    }


    # Set the search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = first_solution_strategies[first_solution_strategy]

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = local_search_strategies[local_search_strategy]
    search_parameters.time_limit.seconds = time_limit

    if log_search:
        search_parameters.log_search = True

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)


    # Print solution on console.
    if print_out_solution:
        print_solution(manager, routing, solution)

    solution_cust_list = get_solution_as_cust_list(customers, manager, routing, solution)

    return solution_cust_list



def print_solution(manager, routing, solution):
        """Prints solution on console."""
        print('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        print(plan_output)
        plan_output += 'Route distance: {}miles\n'.format(route_distance)


def get_solution_as_cust_list(customers, manager, routing, solution):

    index = routing.Start(0)
    solution_list = []
    while not routing.IsEnd(index):
        solution_list.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))

    solution_cust_list = []
    for id in solution_list:
        solution_cust_list.append(customers[id])

    return solution_cust_list


def plot_or_tools_solution(customers, solution, routing, manager):
    pass


def compare_algorithms(customers, distance_matrix, vehicles=1, start_id=0, time_limit=5):

    algorithms = local_search_strategies = ['AUTOMATIC', 'GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING','TABU_SEARCH']
    distances = []


    for algo in algorithms:

        solution = or_tools_tsp_solver(customers, distance_matrix, local_search_strategy=algo, time_limit=time_limit)
        solution_distance_algo = solution_distance(solution, distance_matrix)
        distances.append(solution_distance_algo)

    results = {'Algorithm': algorithms, 'Distance': distances}

    return pd.DataFrame(results)