import numpy as np


def nearest_neighbor(customers):
    solution = []
    current_customer = customers[0]
    solution.append(current_customer)

    for i in range(len(customers)-1):

        distance_to_current_cust = []
        for cust in (customers):
            if cust in solution:
                distance_to_current_cust.append(100000000)
            else:
                distance = cust.dist_to_customer(current_customer)
                distance_to_current_cust.append(distance)
        closest_customer_index = np.argmin(distance_to_current_cust)
        closest_customer = customers[closest_customer_index]

        solution.append(closest_customer)
        current_customer = closest_customer

    return solution