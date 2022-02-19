from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

class Location:

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

    def dist_to_location(self, location):
        distance = math.sqrt(((location.latitude - self.latitude)**2 + (location.longitude - self.longitude)**2))
        distance_rounded = int(round(distance, 0))
        return distance_rounded




class VRP_Problem:

    def __init__(self, n_customers):

        self.locations = []
        self.distance_matrix = []
        self.solution = []
        self.solution_distance = None
        self.max_vehicle_distance = None
        
        self.initialize_problem(n_customers)


    def get_depot(self):
        return self.depot
    
    def get_customers(self):
        return self.customers

    def get_distance_matrix(self):
        return self.distance_matrix
    
    def get_solution(self):
        return self.solution

    def get_solution_distance(self):
        return self.solution_distance
    
    def initialize_problem(self, n_customers):

        # Generate Depot and Customers
        locations = []
        locations.append(Location(0, "Depot", round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2)))
        for i in range(n_customers):
            new_customer = Location(i+1, f"Cust_{i+1}", round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2))
            locations.append(new_customer)

        self.locations = locations

        # Generate distance Matrix

        distance_matrix = np.zeros((n_customers+1, n_customers+1))

        for i, location_from in enumerate(locations):
            for j, location_to in enumerate(locations):
                if i == j:
                    distance_matrix[i, j] = 1000000
                else:
                    distance_matrix[i, j] = location_from.dist_to_location(location_to)
        
        self.distance_matrix = distance_matrix

    
    def solve_problem(self, local_search_strategy='AUTOMATIC', num_vehicles=3, vehicle_max_distance=10000, time_limit=5, span_cost_coef=100, log_search = False):

        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix), num_vehicles, 0)

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

        # Add Distance constraint.
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            vehicle_max_distance,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(span_cost_coef)

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

        routes = []
        route_distances = []
        for route_nbr in range(routing.vehicles()):
            route_distance = 0
            index = routing.Start(route_nbr)
            route = [manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, route_nbr)
                route.append(manager.IndexToNode(index))
            routes.append(route)
            route_distances.append(route_distance)

        


        # Assign values to Class attributes

        self.solution = routes
        self.max_vehicle_distance = max(route_distances)
        self.solution_distance = sum(route_distances)



    def plot_customers_and_depot(self, add_names=False):

        n_locations = len(self.locations)
        names = []
        x = []
        y = []

        for i in range(len(self.locations)):
            names.append(self.locations[i].get_id())
            x.append(self.locations[i].get_longitude())
            y.append(self.locations[i].get_latitude())


        fig = plt.figure()
        plt.plot(x[0], y[0], marker='s', linestyle='None', color='black', markersize=7)
        plt.plot(x[1:], y[1:], marker='o', linestyle='None', color='darkslategray', markersize=5)
        plt.suptitle('Depot and Customers to Visit', fontweight="bold")
        plt.title(f'Number of Customers: {n_locations-1}')

        plt.axis([0, 105, 0, 105])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        if add_names:
            for i, name in enumerate (names):
                plt.text(x[i]+0.2, y[i]+0.3, name)

        return fig;


    def plot_solution(self, algorithm = None, add_names=False):

        colors = ['darkgreen', 'maroon', 'darkgoldenrod', 'royalblue', 'indigo', 'purple', 'grey', 'yellow', 'skyblue', 'lime']

        names = []
        x = []
        y = []
        algorithm = algorithm.replace('_', ' ').title()

        for i in range(len(self.locations)):
            names.append(self.locations[i].get_id())
            x.append(self.locations[i].get_longitude())
            y.append(self.locations[i].get_latitude())


        fig = plt.figure()
        plt.plot(x[0], y[0], marker='s', linestyle='None', color='black', markersize=7)
        plt.plot(x[1:], y[1:], marker='o', linestyle='None', color='darkslategray', markersize=5)
        plt.suptitle(f'Solution found by: {algorithm}', fontweight="bold")
        plt.title(f'Total Distance: {self.solution_distance}km - Max Vehicle Distance: {self.max_vehicle_distance}')

        for i, route in enumerate(self.solution):
            
            for j in range(len(route) - 1):
                first_cust_index = route[j]
                second_cust_index = route[j+1]
                first_cust = self.locations[first_cust_index]
                second_cust = self.locations[second_cust_index]

                x1, x2 = first_cust.get_longitude(), second_cust.get_longitude()
                y1, y2 = first_cust.get_latitude(), second_cust.get_latitude()
                plt.plot([x1,x2],[y1,y2], color=colors[i])



        plt.axis([0, 105, 0, 105])
        ax = plt.gca()
        ax.set_autoscale_on(False)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        if add_names:
            for i, name in enumerate (names):
                plt.text(x[i]+0.2, y[i]+0.3, name)

        


        return fig;