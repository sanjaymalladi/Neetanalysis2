import streamlit as st
import pandas as pd
import pdfplumber
import os

# File path setup
current_dir = os.path.dirname(__file__)  # Gets the directory of the current script
pdf_path = os.path.join(current_dir, "MBBS_BDSCQ_EligibleProvisionalMeritList (2).pdf")

# Extract data from PDF
def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip header
                    data.append(row)
        return data

# Load data from PDF
raw_data = extract_data_from_pdf(pdf_path)

# Convert data to DataFrame
columns = ["S.No", "NEET Roll No", "NEET Rank", "NEET Score", "Name", "Gender", "Category", "Area", "Muslim Minority", "Anglo Indian", "EWS"]
df = pd.DataFrame(raw_data, columns=columns)

# Convert relevant columns to proper types
df["NEET Score"] = pd.to_numeric(df["NEET Score"], errors='coerce')
df["NEET Rank"] = pd.to_numeric(df["NEET Rank"], errors='coerce')

# Streamlit app
st.set_page_config(page_title="Candidate Filter", layout="wide", theme="dark")

st.title("MBBS & BDS Candidates Filter")

# Sidebar filters
gender_filter = st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
category_filter = st.sidebar.multiselect("Category", options=df["Category"].unique(), default=df["Category"].unique())
area_filter = st.sidebar.multiselect("Area", options=df["Area"].unique(), default=df["Area"].unique())
muslim_minority_filter = st.sidebar.multiselect("Muslim Minority", options=df["Muslim Minority"].unique(), default=df["Muslim Minority"].unique())
anglo_indian_filter = st.sidebar.multiselect("Anglo Indian", options=df["Anglo Indian"].unique(), default=df["Anglo Indian"].unique())
ews_filter = st.sidebar.multiselect("EWS", options=df["EWS"].unique(), default=df["EWS"].unique())

# Filter the DataFrame
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Category"].isin(category_filter)) &
    (df["Area"].isin(area_filter)) &
    (df["Muslim Minority"].isin(muslim_minority_filter)) &
    (df["Anglo Indian"].isin(anglo_indian_filter)) &
    (df["EWS"].isin(ews_filter))
]

# Display the number of candidates
st.write(f"Total Number of Candidates: {filtered_df.shape[0]}")

# Optional: Display the filtered DataFrame
# st.write(filtered_df)