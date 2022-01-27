from nearest_neighbor import *
from utility_tsp import *
import random
import math
import numpy as np


def simulated_annealing(customers, distance_matrix, T=100, alpha=0.8, iterations=10000):

    current_tour = nearest_neighbor(customers)
    current_distance = solution_distance(current_tour, distance_matrix)
    best_tour = current_tour
    best_tour_distance = solution_distance(best_tour, distance_matrix)
    N_customers = len(customers)

    
    while T > 1:
        for iter in range(iterations):

            i = random.randint(0, N_customers-2)
            j = random.randint(i + 1, N_customers-1)

            new_route = current_tour[:]
            new_route[i:j] = current_tour[i:j][::-1]
            new_route_distance = solution_distance(new_route, distance_matrix)

            if accept_new_route(new_route_distance, current_distance, T):
                current_tour = new_route
                current_distance = new_route_distance

            if current_distance <= best_tour_distance:
                best_tour = current_tour
                best_tour_distance = current_distance
            
        T = T * alpha
    return best_tour




def accept_new_route(new_route_distance, current_distance, T):

    random_num = random.random()

    if new_route_distance < current_distance:
        return True
    elif random_num < math.exp(-(new_route_distance - current_distance) / T):
        return True
    else:
        return False





def tabu_search(customers, distance_matrix, tabu_length=50, iterations=1000, n_neighbors=200):

    iters = 0
    tabu_list = []
    current_tour = nearest_neighbor(customers)
    best_tour = current_tour
    best_tour_distance = solution_distance(best_tour, distance_matrix)
    N_customers = len(customers)


    for _ in range(iterations):
        neighbor_solutions = []
        neighbor_solutions_distance = []
        for _ in range(n_neighbors):

            # Generate random numbers for neighbor solutions   
            i = random.randint(0, N_customers-2)
            j = random.randint(i + 1, N_customers-1)

            # Create neighbor soultions
            neighbor_solution = current_tour[:]
            neighbor_solution[i:j] = current_tour[i:j][::-1]
            neighbor_distance = solution_distance(neighbor_solution, distance_matrix)

            # Skip neighbor if it is in tabe list
            if neighbor_solution in tabu_list:
                continue
            
            # Otherwise add neighbor to candidate solutions
            neighbor_solutions.append(neighbor_solution)
            neighbor_solutions_distance.append(neighbor_distance)


        if not neighbor_solutions:
            continue
        
        # Find best neighbor
        best_neighbor_index = np.argmin(neighbor_solutions_distance)
        best_neighbor = neighbor_solutions[best_neighbor_index]

        # Update the current tour to the best neighbor
        current_tour = best_neighbor

        # Add current tour to tabu_list and remove first element if list is full
        if len(tabu_list) == tabu_length:
            del tabu_list[0]
        
        tabu_list.append(current_tour)

        # If best neighbor is better than our current best, update current best

        if neighbor_solutions_distance[best_neighbor_index] < best_tour_distance:
            best_tour = best_neighbor
            best_tour_distance = neighbor_solutions_distance[best_neighbor_index]


    return best_tour

