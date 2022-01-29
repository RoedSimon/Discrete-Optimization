
import streamlit as st
import pandas as pd
import numpy as np
from solver_functions.TSP_solvers.or_tools_tsp import *
from solver_functions.TSP_solvers.utility_tsp import *

st.set_page_config(layout="wide")

st.title('Travelling Salesman Problem')

st.markdown("### Description text here")


st.sidebar.markdown("## Select Number of Customers")
number_of_customers = st.sidebar.slider("Number of Customer Location to Visit", min_value=50, max_value=200)


customers = create_customers(number_of_customers)


st.sidebar.markdown("## Select Algoritm and Settings")
algorithm_selected = st.sidebar.selectbox("Choose an Algoritm", 
['AUTOMATIC', 'GREEDY_DESCENT', 'GUIDED_LOCAL_SEARCH', 'SIMULATED_ANNEALING', 'TABU_SEARCH'])
time_limit_slider = st.sidebar.slider("Max time to solve problem (seconds)", min_value=1, max_value=10, value=2)




distance_matrix = create_distance_matrix(customers)
solution = or_tools_tsp_solver(customers, distance_matrix, vehicles=1, start_id=0, first_solution_strategy='AUTOMATIC',
                                local_search_strategy=algorithm_selected, time_limit=time_limit_slider)
customers_plot = plot_solution_or(customers, distance_matrix, show_route=True)
solution_plot = plot_solution_or(solution, distance_matrix)


col1, col2 = st.columns(2)

with col1:
    st.header('Random Solution')
    st.pyplot(customers_plot)

with col2:
    st.header('Optimized Solution')
    st.pyplot(solution_plot)




DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
