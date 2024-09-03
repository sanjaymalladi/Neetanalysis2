import streamlit as st
import pandas as pd
import pdfplumber
import os

# Load the CSV file
file_path = 'output_final.csv'
df = pd.read_csv(file_path)

# Set up the page configuration
st.set_page_config(page_title="Candidate Filter", layout="wide", initial_sidebar_state="expanded")

# Function to apply filters to the dataframe
def apply_filters(df):
    filtered_df = df.copy()
    
    # Add score filter
    min_score, max_score = st.sidebar.slider(
        "Filter by Score",
        min_value=float(df['NEET Score'].min()),
        max_value=float(df['NEET Score'].max()),
        value=(float(df['NEET Score'].min()), float(df['NEET Score'].max()))
    )
    filtered_df = filtered_df[(filtered_df['NEET Score'] >= min_score) & (filtered_df['NEET Score'] <= max_score)]
    
    # Create filters for each column if applicable
    for column in df.columns:
        if column != 'NEET Score':  # Skip 'Score' as we've already handled it
            unique_values = df[column].dropna().unique()
            if len(unique_values) < 50:  # Filter only if unique values are manageable
                selected_values = st.sidebar.multiselect(f"Filter by {column}", unique_values)
                if selected_values:
                    filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    
    return filtered_df

# Apply filters
st.sidebar.header("Filters")
filtered_df = apply_filters(df)

# Display the total number of candidates based on the selected filters
total_candidates = filtered_df.shape[0]
st.header(f"Total Number of Candidates: {total_candidates}")

# Display relevant demographics
st.subheader("Demographics")

# Gender distribution
gender_distribution = filtered_df['Gender'].value_counts()
st.bar_chart(gender_distribution)

# Category distribution
category_distribution = filtered_df['Category'].value_counts()
st.bar_chart(category_distribution)

# Area distribution
area_distribution = filtered_df['Area'].value_counts()
st.bar_chart(area_distribution)

# Muslim Minority distribution
muslim_minority_distribution = filtered_df['Muslim Minority'].value_counts()
st.bar_chart(muslim_minority_distribution)

# Anglo Indian distribution
anglo_indian_distribution = filtered_df['Anglo Indian'].value_counts()
st.bar_chart(anglo_indian_distribution)

# EWS distribution
ews_distribution = filtered_df['EWS'].value_counts()
st.bar_chart(ews_distribution)
