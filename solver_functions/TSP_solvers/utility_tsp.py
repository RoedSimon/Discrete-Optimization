import math
import random
import numpy as np
import seaborn as sns
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
        distance_rounded = round(distance, 2)
        return distance_rounded



@st.cache
def create_customers(n):
    customers = []
    for i in range(n):
        new_customer = Customer(i, f"Cust_{i}", round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2))
        customers.append(new_customer)
    return customers


def create_distance_matrix(customers):
    n_customers = len(customers)
    distance_matrix = np.zeros((n_customers, n_customers))

    for i, cust_from in enumerate(customers):
        for j, cust_to in enumerate(customers):
            if i == j:
                distance_matrix[i, j] = 1000000
            else:
                distance_matrix[i, j] = cust_from.dist_to_customer(cust_to)

    return distance_matrix



def solution_distance(solution, distance_matrix):
    total_distance = 0
    n_customers = len(solution)

    for i, cust in enumerate(solution):
        if i == n_customers-1:
            total_distance += distance_matrix[cust.get_id(), solution[0].get_id()]
        else:
            total_distance += distance_matrix[cust.get_id(), solution[i+1].get_id()]
            
    return round(total_distance, 2)




def plot_solution(solution, distance_matrix, add_names=False, show_route=True):
    

    route_distance = solution_distance(solution, distance_matrix)
    n_cust = len(solution)
    names = []
    x = []
    y = []

    for cust in solution:
        names.append(cust.get_id())
        x.append(cust.get_longitude())
        y.append(cust.get_latitude())
    
    
    plt.plot(x, y, 'ko', markersize = 3)
    plt.suptitle('Travelling Salesman Tour', fontweight="bold")
    plt.title(f'Customers: {n_cust} - Distance: {route_distance}')
    #plt.title(f'Travelling Salesman Tour\n Customers: {n_cust} - Distance: {route_distance}')

    plt.axis([0, 100, 0, 100])
    ax = plt.gca()
    ax.set_autoscale_on(False)

    if add_names:
        for i, name in enumerate (names):
            plt.text(x[i]+0.2, y[i]+0.3, name)
    
    if show_route:
        plot_solution = solution.copy()
        plot_solution.append(plot_solution[0])
        for i in range(n_cust):

            first_cust = plot_solution[i]
            if i == n_cust:
                second_cust = plot_solution[0]
            else:
                second_cust = plot_solution[i+1]

            x1, x2 = first_cust.get_longitude(), second_cust.get_longitude()
            y1, y2 = first_cust.get_latitude(), second_cust.get_latitude()
            plt.plot([x1,x2],[y1,y2],'k-')

    return plt.show(); 


def plot_solution_or(solution, distance_matrix, add_names=False, show_route=True):
    

    fig = plt.figure()
    #fig.set_facecolor("#f0f2f6")
    route_distance = solution_distance(solution, distance_matrix)
    n_cust = len(solution)
    names = []
    x = []
    y = []

    for cust in solution:
        names.append(cust.get_id())
        x.append(cust.get_longitude())
        y.append(cust.get_latitude())

    if show_route:
        plot_solution = solution.copy()
        plot_solution.append(plot_solution[0])
        for i in range(n_cust):

            first_cust = plot_solution[i]
            if i == n_cust:
                second_cust = plot_solution[0]
            else:
                second_cust = plot_solution[i+1]

            x1, x2 = first_cust.get_longitude(), second_cust.get_longitude()
            y1, y2 = first_cust.get_latitude(), second_cust.get_latitude()
            plt.plot([x1,x2],[y1,y2], color="darkgreen")
    
    
    plt.plot(x, y, marker='o', linestyle='None', color='darkslategray', markersize = 5)
    plt.suptitle('Travelling Salesman Tour', fontweight="bold")
    plt.title(f'Customers: {n_cust} - Distance: {route_distance}')
    #plt.title(f'Travelling Salesman Tour\n Customers: {n_cust} - Distance: {route_distance}')

    plt.axis([0, 105, 0, 105])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    #ax.set_facecolor("#f0f2f6")
    #ax.axis("off")

    if add_names:
        for i, name in enumerate (names):
            plt.text(x[i]+0.2, y[i]+0.3, name)

    return fig; 