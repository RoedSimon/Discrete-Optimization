from utility_tsp import solution_distance
from nearest_neighbor import nearest_neighbor
from numpy import argmin



def two_opt_swap(route, i, j, distance_matrix):

    customers = len(route)
    best_tour = route
    best_distance = solution_distance(route)

    return best_tour



def two_opt(route, distance_matrix, iteration_limit = None):

    route = nearest_neighbor(route)
    customers = len(route)
    best_tour = route
    improved = True
    iterations = 0

    while improved:
        improved = False
        for i in range(customers - 1):
            for j in range(i + 1, customers):
                if j-i==1: continue # We would not change anything, so we skip it
                new_route = route[:]
                new_route[i:j] = route[i:j][::-1] # perform 2-opt swap by reversing the selected part
                iterations += 1
                if solution_distance(new_route, distance_matrix) < solution_distance(best_tour, distance_matrix):
                    best_tour = new_route
                    improved = True

        route = best_tour
    #print('Two-Opt iterations: ', iterations)
    return best_tour

def three_opt(route, distance_matrix, iteration_limit = None):

    route = nearest_neighbor(route)
    customers = len(route)
    best_tour = route
    improved = True
    iterations = 0

    while improved:
        improved = False
        for i in range(customers - 1):
            for j in range(i + 1, customers):
                if j-i==1: continue # We would not change anything, so we skip it

                sub_1 = route[:][0:i]
                sub_2 = route[:][i:j]
                sub_3 = route[:][j:]

                new_routes = []
                new_routes.append(sub_1 + sub_2 + sub_3[::-1])
                new_routes.append(sub_1 + sub_2[::-1] + sub_3)
                new_routes.append(sub_1 + sub_3[::-1] + sub_2[::-1])
                new_routes.append(sub_1 + sub_3[::1] + sub_2)
                new_routes.append(sub_1 + sub_3 + sub_2[::-1])
                new_routes.append(sub_1 + sub_2[::-1] + sub_3[::-1])
                new_routes.append(sub_1 + sub_3 + sub_2)

                iterations += 1
                
                new_routes_cost = []
                for new_route in new_routes:
                    new_routes_cost.append(solution_distance(new_route, distance_matrix))

                best_new_route_index = argmin(new_routes_cost) 

                if new_routes_cost[best_new_route_index] < solution_distance(best_tour, distance_matrix):
                    best_tour = new_routes[best_new_route_index]
                    improved = True

        route = best_tour
    #print('Three-Opt iterations: ', iterations)
    return best_tour


