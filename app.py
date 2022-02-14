
import streamlit as st
from solver_functions.TSP_solvers.or_tools_tsp import TSP_Problem


## Title and Header information ##

st.set_page_config(page_title='Traveling Salesman Problem', layout='wide')

st.title('Travelling Salesman Problem')

st.markdown('###### *The travelling salesman problem asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"*')

## Sidebar Selection Panel ##

st.sidebar.markdown('*Adjust the settings to set the problem size and algorithm*')

st.sidebar.markdown("## Select Number of Customers")
number_of_customers = st.sidebar.slider("Number of Customer Location to Visit", min_value=50, max_value=250)

st.sidebar.markdown("## Select Algoritm and Settings")
algorithm_selected = st.sidebar.selectbox("Choose an Algoritm", 
['GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING', 'TABU_SEARCH'])


time_limit_slider = st.sidebar.slider("Max time to solve problem (seconds)", min_value=1, max_value=10, value=1)


## Create TSP_Problem instance and solve it ##

tsp_problem = TSP_Problem(number_of_customers)
tsp_problem.solve_problem(local_search_strategy=algorithm_selected, time_limit=time_limit_slider)


## Set Page Layout ##

col1, col2 = st.columns(2)


# Show plots

with col1:
    st.pyplot(tsp_problem.plot_customers())


with col2:
    st.pyplot(tsp_problem.plot_solution(algorithm_selected))


