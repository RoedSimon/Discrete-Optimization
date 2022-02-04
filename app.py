
import streamlit as st
import pandas as pd
import numpy as np
from solver_functions.TSP_solvers.or_tools_tsp import *
from solver_functions.TSP_solvers.utility_tsp import *


## Title and Header information ##

st.set_page_config(layout="wide")

st.title('Travelling Salesman Problem')

st.markdown("### Description text here")

## Sidebar Selection Panel ##

st.sidebar.markdown("## Select Number of Customers")
number_of_customers = st.sidebar.slider("Number of Customer Location to Visit", min_value=50, max_value=200)

st.sidebar.markdown("## Select Algoritm and Settings")
algorithm_selected = st.sidebar.selectbox("Choose an Algoritm", 
['AUTOMATIC', 'GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING', 'TABU_SEARCH'])

time_limit_slider = st.sidebar.slider("Max time to solve problem (seconds)", min_value=1, max_value=10, value=1)

## Create Data and Customer Plot ##

customers = create_customers(number_of_customers)
distance_matrix = create_distance_matrix(customers)
customers_plot = plot_solution_or(customers, distance_matrix, show_route=False)


## Set Page Layout ##

col1, col2 = st.columns(2)

# Solve Problem and generate plot

 
solution = or_tools_tsp_solver(customers, distance_matrix, vehicles=1, start_id=0, first_solution_strategy='AUTOMATIC',
                                        local_search_strategy=algorithm_selected, time_limit=time_limit_slider)

solution_plot = plot_solution_or(solution, distance_matrix)


# Show plots

with col1:
        st.header('Customers To Visit')
        st.pyplot(customers_plot)


with col2:
    st.header('Optimized Solution')
    st.pyplot(solution_plot)


if


