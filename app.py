

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model import preprocess_data, get_summary, create_dataframe_from_input


# Page Configuration

st.set_page_config(page_title="Student Marks Summary", layout="centered")


# Here i have applied some CSS that makes the page good

custom_css = """
<style>
    body {
        background-color: #f6f6f6;
        color: #31333F;
    }

    .title {
        font-size: 36px !important;
        color: #4B8BBE;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    .subheader {
        font-size: 22px !important;
        color: #306998;
        font-weight: 600;
        margin-top: 20px;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #1E3A8A; /* deep blue */
        color: white;
        border: none;
        padding: 0.65rem 1.5rem;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 800; /* BOLD */
        transition: 0.3s ease;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3);
    }

    .stButton > button:hover {
        background-color: #2563EB; /* lighter blue */
        color: #fff;
        transform: scale(1.04);
        cursor: pointer;
    }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)


#  Title of the Project

st.markdown('<div class="title"> Student Marks and Grades Summary</div>', unsafe_allow_html=True)


# Sidebar: File Upload

st.sidebar.header("📥 Upload CSV")
uploaded_file = st.sidebar.file_uploader("Upload student_marks.csv", type="csv")


# Code that shows Report and Charts

def show_summary(df):
    st.markdown('<div class="subheader">📄 Student Report</div>', unsafe_allow_html=True)
    st.dataframe(df.style.format({'Average': "{:.2f}"}))

    class_avg, topper = get_summary(df)

    st.success(f"📊 Class Average: {class_avg:.2f}")
    st.info("🏆 Topper(s):")
    st.dataframe(topper[['Name', 'Average', 'Grade']])

    st.markdown('<div class="subheader">📊 Average Marks per Student</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.barplot(x='Name', y='Average', data=df, palette='viridis', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)


# CSV Upload Logic

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df = preprocess_data(df)
        show_summary(df)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

else:
    st.markdown('<div class="subheader"> Or Enter Data Manually</div>', unsafe_allow_html=True)
    with st.form("manual_input_form"):
        num_students = st.number_input("Number of Students", min_value=1, max_value=20, step=1)
        names, marks1, marks2, marks3 = [], [], [], []

        for i in range(int(num_students)):
            st.markdown(f"**Student {i+1} Details**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                name = st.text_input(f"Name", key=f"name_{i}")
            with col2:
                m1 = st.number_input(f"Subject 1", min_value=0, max_value=100, key=f"m1_{i}")
            with col3:
                m2 = st.number_input(f"Subject 2", min_value=0, max_value=100, key=f"m2_{i}")
            with col4:
                m3 = st.number_input(f"Subject 3", min_value=0, max_value=100, key=f"m3_{i}")

            names.append(name)
            marks1.append(m1)
            marks2.append(m2)
            marks3.append(m3)

        submit = st.form_submit_button(" Generate Report")

    if submit:
        try:
            df = create_dataframe_from_input(names, marks1, marks2, marks3)
            show_summary(df)
        except Exception as e:
            st.error(f"⚠️ Error in manual input: {e}")
