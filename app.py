
import streamlit as st
from solvers.or_tools_tsp import TSP_Problem
from solvers.or_tools_vrp import VRP_Problem

st.set_page_config(page_title='Discrete Optimization App', layout='wide')

st.sidebar.markdown("## App Navigation")
app_navigation = st.sidebar.selectbox('', 
                                ['Travelling Salesman Problem', 'Vehicle Routing Problem'])

if app_navigation == 'Travelling Salesman Problem':

    ## Title and Header information ##

    st.title('Travelling Salesman Problem')

    st.markdown('###### *The travelling salesman problem asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"*')

    ## Sidebar Selection Panel ##

    #st.sidebar.markdown('*Adjust the settings to set the problem size and algorithm*')
    st.sidebar.markdown('')

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


elif app_navigation == 'Vehicle Routing Problem':

    ## Title and Header information ##

    st.title('Vehicle Routing Problem')

    st.markdown('###### *The vehicle routing problem asks the following question: "What is the optimal set of routes for a fleet of vehicles to traverse in order to deliver to a given set of customers such that the length of the longest route is minimized?"*')

    ## Sidebar Selection Panel ##

    #st.sidebar.markdown('*Adjust the settings to set the problem size and algorithm*')
    st.sidebar.markdown('')

    st.sidebar.markdown("## Select Number of Customers")
    number_of_customers = st.sidebar.slider("Number of Customer Location to Visit", min_value=25, max_value=75, value=50)

    st.sidebar.markdown("## Select Number of Vehicles")
    number_of_vehicles = st.sidebar.slider("Number of Vehicles", min_value=2, max_value=5, value=2)

    st.sidebar.markdown("## Select Algoritm and Settings")
    algorithm_selected = st.sidebar.selectbox("Choose an Algoritm", 
    ['GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING', 'TABU_SEARCH'])


    time_limit_slider = st.sidebar.slider("Max time to solve problem (seconds)", min_value=1, max_value=30, value=2)


    ## Create VRP_Problem instance and solve it ##

    vrp_problem = VRP_Problem(number_of_customers)
    vrp_problem.solve_problem(local_search_strategy=algorithm_selected, num_vehicles=number_of_vehicles, time_limit=time_limit_slider)


    ## Set Page Layout ##

    col1, col2 = st.columns(2)


    # Show plots

    with col1:
        st.pyplot(vrp_problem.plot_customers_and_depot())


    with col2:
        st.pyplot(vrp_problem.plot_solution(algorithm_selected))