# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")


with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    M = st.text_input("How many calories did you eat on Monday?")

    M2 = st.text_input("How many calories did you eat on Tuesday?")

    M3 = st.text_input("How many calories did you eat on Wednesday?")

    M4 = st.text_input("How many calories did you eat on Thursday?")

    M5 = st.text_input("How many calories did you eat on Friday?")
    M6 = st.text_input("How many calories did you eat on Saturday?")

    M7 = st.text_input("How many calories did you eat on Sunday?")

    submitted = st.form_submit_button("Submit Data")
    

if submitted:
    file_exists = os.path.isfile("data.csv")
    infile = open("data.csv", "w")    

    if file_exists:
        infile.write(f"Day,Calories\n Monday,{M}\nTuesday,{M2}\nWednesday,{M3}\nThursday,{M4}\n Friday,{M5}\nSaturday,{M6}\nSunday,{M7}\n")
    infile.close()
    
    st.success("Your data has been submitted!")

else:
    st.warning("Please fill in both fields before submitting.")

st.divider() 
st.header("Current Data in CSV")

if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

