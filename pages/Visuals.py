

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.


st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)


st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")



st.divider()
st.header("Load Data")

try:
    if os.path.exists("data.xlsx"):
        df = pd.read_csv("data.xlsx")
        st.success("CSV data loadeded")
        st.dataframe(df.head())
    else:
        os.path.getsize('data.csv')
        df = pd.DataFrame()
except Exception as e:
    st.error(f"Error {e}")
    df = pd.DataFrame()

try:
    if os.path.exists("data.json"):
        with open ("data.json",  "r") as json_file:
            json_data = json.load(json_file)
        st.success("JSON data loaded successfully!")

    else:
        st.warning("data.json file not found.")
        json_data = {}
except Exception as e:
    st.error(f"Error loading JSON file: {e}")
    json_data = {}


st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH (JSON file)
st.subheader("Graph 1: Weekly Calorie Intake") # CHANGE THIS TO THE TITLE OF YOUR GRAPH

try:
    infile = open("data.json", "r")
    json_data = json.load(infile)
    infile.close()
    data_points = json_data.get("data_points", [])
    df = pd.DataFrame(data_points)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if len(df) == len(weekdays):
        df["Days"] = weekdays
    st.write("Loaded data preview:")
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Error loading JSON file or creating chart: {e}")
    st.warning("Make sure your JSON has the structure with 'data_points' inside it.")
    
st.bar_chart(df.set_index("Days")["Calories"]) # NEW

st.write("""
This static bar chart shows the number of calories consumed each day from Monday to Sunday.
It uses data loaded from your 'data.json' file.
""")


# GRAPH 2: DYNAMIC GRAPH (JSON file)
st.subheader("Graph 2: Select days to View Calories") # CHANGE THIS TO THE TITLE OF YOUR GRAPH

try:
    infile = open("data.json", "r")
    json_data = json.load(infile)
    infile.close()
    data_points= json_data.get("data_points", [])
    df = pd.DataFrame(data_points)

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if len(df) == len(weekdays):
        df["Days"] = weekdays  
    st.write("### Choose which days you want to display:")
    selected_days = st.multiselect(
    "Select one or more days:",
    options=df["Days"].tolist(),
    default=df["Days"].tolist()
)
    filtered_df = df[df["Days"].isin(selected_days)]
    st.line_chart(data=filtered_df, x="Days", y="Calories") # NEW

    st.write("""
This dynamic line chart updates based on which days you select above.
It uses Streamlit widgets to make the visualizations interactive.
""")
except Exception as e:
    st.error("error loading JSON file or creating chart: {e}")
    st.warning("Make sure your JSON has the structure with 'data_points' inside it.")

# GRAPH 3: DYNAMIC GRAPH (XLSX file)
import matplotlib.pyplot as plt
st.subheader("Graph 3: Filter Daily Calories by Minimum Amount")

# --- Load data ---
try:

    df = pd.read_csv("data.csv")  # Make sure data.xlsx is in the same folder
except FileNotFoundError:
    st.error("The file 'data.xlsx' was not found. Make sure it's in the same folder as this script.")
    st.stop()
except Exception as e:
    st.error(f"Error loading or processing the file: {e}")
    st.stop()
df.columns = ["Day", "Calories"]
if "min_caories" not in st.session_state:
    st.session_state.min_calories = 0  # NEW

min_calories = st.slider(
    "Minimum calories to display:",
    0,
    int(df["Calories"].max()) if not df.empty else 5000,
    st.session_state.min_calories
)
st.session_state.min_calories = min_calories

filtered_df = df[df["Calories"] >= st.session_state.min_calories]

if not filtered_df.empty:
    fig, ax = plt.subplots()
    ax.scatter(filtered_df["Day"], filtered_df["Calories"], s=100, color="blue")
    ax.set_title("Filtered Days by Minimum Calories")
    ax.set_xlabel("Day")
    ax.set_ylabel("Calories")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write(f"Showing days where calories ≥ **{st.session_state.min_calories}**.")
else:
    st.warning("No days meet the minimum")

st.write("This graph shows a scatter plot displaying the distrabution of calories eaten in a week. The graph is dynamic as it allows users to decide the lower limit of the data allowing you to identify outliers above certain points")
