import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
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

# Main Streamlit application
def main():
    st.title("Employee Data")

    # Create connection to PostgreSQL
    conn = create_connection()

    # Load data
    data = fetch_data(conn)
    st.write("### Table")
    st.write(data)

    # Filter options
    department_filter = st.selectbox("Filter by Department", options=data['department'].unique())
    filtered_data = data[data['department'] == department_filter]

    st.write(f"### Filtered table - Department: {department_filter}")
    st.write(filtered_data)

    # Save filtered data to CSV
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
