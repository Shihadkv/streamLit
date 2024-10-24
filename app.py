import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# Connect to PostgreSQL

load_dotenv()
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="college",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

# Fetch data from PostgreSQL
def fetch_data(conn):
    query = "SELECT * FROM employees"
    return pd.read_sql(query, conn)




# # Simulate some data
# np.random.seed(42)
# data = pd.DataFrame({
#     'Category': np.random.choice(['A', 'B', 'C'], size=100),
#     'Values': np.random.randint(1, 100, size=100),
#     'Date': pd.date_range('2023-01-01', periods=100, freq='D')
# })

# # Add a title
# st.title("Streamlit List, Graph, and Pagination Example")

# # Filter by Category
# category = st.selectbox("Select a Category", options=data['Category'].unique(), index=0)
# filtered_data = data[data['Category'] == category]

# # Pagination variables
# items_per_page = st.slider("Items per page", min_value=5, max_value=20, value=10)
# total_items = len(filtered_data)
# total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)

# # Select the page number
# page = st.number_input("Select page", min_value=1, max_value=total_pages, value=1)

# # Calculate start and end indices for pagination
# start_idx = (page - 1) * items_per_page
# end_idx = start_idx + items_per_page
# paginated_data = filtered_data.iloc[start_idx:end_idx]

# # Display the paginated list
# st.write(f"Showing items {start_idx + 1} to {min(end_idx, total_items)} out of {total_items}")
# st.dataframe(paginated_data)

# # Display the graph (for all data, or filter based on category)
# st.line_chart(filtered_data[['Date', 'Values']].set_index('Date'))

# # Optional: Add download button for filtered data
# csv = filtered_data.to_csv(index=False)
# st.download_button(label="Download CSV", data=csv, mime='text/csv')





# Generate example data
# np.random.seed(42)
# data = pd.DataFrame({
#     'Category': np.random.choice(['A', 'B', 'C'], size=100),
#     'Values': np.random.randint(1, 100, size=100),
#     'Date': pd.date_range('2023-01-01', periods=100, freq='D')
# })

# # Add title
# st.title("Streamlit Data Viewer with Filters, Pagination, and Bar Chart")

# # Date range filter
# start_date, end_date = st.date_input(
#     "Select date range:",
#     [datetime(2023, 1, 1), datetime(2023, 4, 10)]
# )

# # Filter data based on date range
# filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

# # Numeric filter for Values
# value_threshold = st.slider("Filter values greater than:", min_value=0, max_value=100, value=30)
# filtered_data = filtered_data[filtered_data['Values'] > value_threshold]

# # Pagination variables
# items_per_page = st.slider("Items per page", min_value=5, max_value=20, value=10)
# total_items = len(filtered_data)
# total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)

# # Pagination control with buttons
# page = st.session_state.get("page", 1)

# # Show previous and next buttons
# col1, col2 = st.columns([1, 1])

# if col1.button("Previous") and page > 1:
#     page -= 1
#     st.session_state["page"] = page

# if col2.button("Next") and page < total_pages:
#     page += 1
#     st.session_state["page"] = page

# # Calculate start and end indices for pagination
# start_idx = (page - 1) * items_per_page
# end_idx = start_idx + items_per_page
# paginated_data = filtered_data.iloc[start_idx:end_idx]

# # Show pagination info
# st.write(f"Showing items {start_idx + 1} to {min(end_idx, total_items)} out of {total_items}")

# # Display the paginated list
# st.dataframe(paginated_data)

# # Display the bar chart
# st.bar_chart(paginated_data[['Date', 'Values']].set_index('Date'))

# # Optional: Add download button for filtered data
# csv = filtered_data.to_csv(index=False)
# st.download_button(label="Download Filtered Data", data=csv, mime='text/csv')

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Page config for a better appearance
st.set_page_config(page_title="Professional Dashboard", layout="wide")

# Example data with a Date column
data = pd.DataFrame({
    'Date': pd.date_range(start="2024-01-01", periods=10, freq='D'),
    'Category': ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B'],
    'Values': [50, 40, 70, 90, 55, 35, 60, 100, 65, 45]
})

# Sidebar for global filters
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Dashboard", "User Form", "To-Do List", "Data & Charts", "Filters"])

# Global Filters
st.sidebar.markdown("## Global Filters")

# Date range filter (for date-based data)
date_filter = st.sidebar.date_input(
    "Select a date range",
    [data['Date'].min(), data['Date'].max()]
)

# Category filter (for category-based data)
category_filter = st.sidebar.multiselect(
    "Filter by Category", 
    options=data['Category'].unique(), 
    default=data['Category'].unique()
)

# Apply global filters to the dataset
filtered_data = data[
    (data['Date'] >= pd.to_datetime(date_filter[0])) &
    (data['Date'] <= pd.to_datetime(date_filter[1])) &
    (data['Category'].isin(category_filter))
]

# Header
st.title("Professional Dashboard")
st.markdown("Welcome to your interactive and user-friendly dashboard!")

# Dashboard section with KPIs and chart
if options == "Dashboard":
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    # KPIs based on filtered data
    with col1:
        total_value = filtered_data['Values'].sum()
        st.metric(label="Total Value", value=f"${total_value}")

    with col2:
        category_count = len(filtered_data['Category'].unique())
        st.metric(label="Unique Categories", value=category_count)

    with col3:
        avg_value = filtered_data['Values'].mean() if not filtered_data.empty else 0
        st.metric(label="Average Value", value=f"${avg_value:.2f}")

    # Bar chart with filtered data
    st.markdown("### Filtered Category-wise Performance")
    fig = px.bar(
        filtered_data, x='Category', y='Values', color='Category', 
        title="Category Performance Overview (Filtered)"
    )
    st.plotly_chart(fig, use_container_width=True)

# Data & Charts section
if options == "Data & Charts":
    st.markdown("### 📊 Data & Charts")
    st.write("Analyze and visualize your data with interactive charts.")

    # Show filtered data
    rows = st.slider("Select number of rows to display", min_value=5, max_value=20, value=10)
    st.dataframe(filtered_data.head(rows))
    
    st.markdown("### Filtered Interactive Chart")
    fig = px.line(
        filtered_data, x='Date', y='Values', color='Category', 
        title="Interactive Line Chart (Filtered)"
    )
    st.plotly_chart(fig, use_container_width=True)

# To-Do List section
if options == "To-Do List":
    st.markdown("### 📝 To-Do List")
    st.write("Manage your tasks efficiently with the To-Do List.")
    
    # Input for new task
    new_task = st.text_input("Add a new task", "")
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    # Add new task to the list
    if st.button("Add Task"):
        if new_task:
            st.session_state.tasks.append(new_task)
            st.success(f"Task '{new_task}' added!")
        else:
            st.error("Please enter a task before adding.")

    # Display task list with delete option
    st.write("### Your Tasks:")
    if st.session_state.tasks:
        for idx, task in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"- {task}")
            with col2:
                if st.button(f"Delete {idx}", key=f"delete_{idx}"):
                    del st.session_state.tasks[idx]
                    st.experimental_rerun()
    else:
        st.write("No tasks yet.")

# User Form section
if options == "User Form":
    st.markdown("### 📝 User Form")
    st.write("Please fill in your details below.")
    
    # Form fields
    with st.form("user_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success(f"Thank you, {name}. Your data has been submitted successfully!")
            st.write(f"Name: {name}, Email: {email}, Age: {age}")

# Filters section
if options == "Filters":
    st.markdown("### 🔍 Filter Data")
    st.write("Use global filters (date range and category) to analyze data.")

    # Filtered table with global filters applied
    st.write(f"Filtered data from {date_filter[0]} to {date_filter[1]} for selected categories:")
    st.dataframe(filtered_data)
    
    # Filtered bar chart
    st.markdown("### Filtered Chart by Category")
    fig = px.bar(filtered_data, x='Category', y='Values', color='Category')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© 2024 Shihad Dashboard. All rights reserved.")


