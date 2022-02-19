from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st



class Customer:

    def __init__(self, id, name, latitude, longitude):
        
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def dist_to_customer(self, customer):
        distance = math.sqrt(((customer.latitude - self.latitude)**2 + (customer.longitude - self.longitude)**2))
        distance_rounded = int(round(distance, 0))
        return distance_rounded


@st.cache(allow_output_mutation=True)
class TSP_Problem:

    def __init__(self, n_customers):

        self.customers = []
        self.distance_matrix = []
        self.solution = []
        self.solution_distance = None
        
        self.initialize_problem(n_customers)


    def get_customers(self):
        return self.customers

    def get_distance_matrix(self):
        return self.distance_matrix
    
    def get_solution(self):
        return self.solution

    def get_solution_distance(self):
        return self.solution_distance
    
    def initialize_problem(self, n_customers):
        
        # Generate Customers
        customers = []
        for i in range(n_customers):
            new_customer = Customer(i, f"Cust_{i}", round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2))
            customers.append(new_customer)
        
        self.customers = customers

        # Generate distance Matrix

        distance_matrix = np.zeros((n_customers, n_customers))

        for i, cust_from in enumerate(customers):
            for j, cust_to in enumerate(customers):
                if i == j:
                    distance_matrix[i, j] = 1000000
                else:
                    distance_matrix[i, j] = cust_from.dist_to_customer(cust_to)
        
        self.distance_matrix = distance_matrix

    
    def solve_problem(self, local_search_strategy='AUTOMATIC', time_limit=5, log_search = False):

        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix), 1, 0)

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        #Define possible possible search strategies
        local_search_strategies = {
        'AUTOMATIC' : routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC,
        'GREEDY_DESCENT' : routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT,
        'GUIDED_LOCAL_SEARCH' : routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
        'SIMULATED_ANNEALING' : routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
        'TABU_SEARCH' : routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
        }

        # Set the search parameters.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
        search_parameters.local_search_metaheuristic = local_search_strategies[local_search_strategy]
        search_parameters.time_limit.seconds = time_limit

        if log_search:
            search_parameters.log_search = True

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)


        # Get solution as list

        index = routing.Start(0)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))

        # Assign values to Class attributes

        self.solution = route
        self.solution_distance = solution.ObjectiveValue()



    def plot_customers(self, add_names=False):

        n_cust = len(self.solution)-1
        names = []
        x = []
        y = []

        for cust in self.solution:
            names.append(self.customers[cust].get_id())
            x.append(self.customers[cust].get_longitude())
            y.append(self.customers[cust].get_latitude())


        fig = plt.figure()
        plt.plot(x, y, marker='o', linestyle='None', color='darkslategray', markersize = 5)
        plt.suptitle('Customers to Visit', fontweight="bold")
        plt.title(f'Number of Customers: {n_cust}')

        plt.axis([-5, 105, -5, 105])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        if add_names:
            for i, name in enumerate (names):
                plt.text(x[i]+0.2, y[i]+0.3, name)

        return fig;


    def plot_solution(self, algorithm = None, add_names=False):

        n_cust = len(self.solution)
        names = []
        x = []
        y = []
        algorithm = algorithm.replace('_', ' ').title()

        for cust in self.solution:
            names.append(self.customers[cust].get_id())
            x.append(self.customers[cust].get_longitude())
            y.append(self.customers[cust].get_latitude())


        fig = plt.figure()

        for i in range(n_cust - 1):

            first_cust = self.customers[self.solution[i]]
            second_cust = self.customers[self.solution[i+1]]

            x1, x2 = first_cust.get_longitude(), second_cust.get_longitude()
            y1, y2 = first_cust.get_latitude(), second_cust.get_latitude()
            plt.plot([x1,x2],[y1,y2], color="darkgreen")

        plt.plot(x, y, marker='o', linestyle='None', color='darkslategray', markersize = 5)
        plt.suptitle(f'Solution found by: {algorithm}', fontweight="bold")
        plt.title(f'Distance: {self.solution_distance}km')

        plt.axis([0, 105, 0, 105])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        if add_names:
            for i, name in enumerate (names):
                plt.text(x[i]+0.2, y[i]+0.3, name)

        


        return fig;