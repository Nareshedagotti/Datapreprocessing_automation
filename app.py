import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App
st.title("Data Preprocessing and Dashboard Automation")

# File upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load the data
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    st.subheader("Uploaded Data")
    st.write(data.head())

    # Data Preprocessing
    st.subheader("Data Preprocessing")
    
    # Remove duplicates
    data = data.drop_duplicates()
    st.write("Removed duplicates, remaining rows:", len(data))
    
    # Handle missing values (fill with mean for numeric columns)
    if data.isnull().sum().sum() > 0:
        data = data.fillna(data.mean(numeric_only=True))
        st.write("Filled missing values in numeric columns with mean")

    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Dashboard with graphs
    st.subheader("Dashboard")

    # 1. Histogram for numerical data
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        st.write("Histogram")
        for col in numeric_columns:
            fig, ax = plt.subplots()
            ax.hist(data[col], bins=20, color="skyblue")
            ax.set_title(f"Histogram of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
    else:
        st.write("No numeric columns for histograms.")

    # 2. Bar chart for categorical data
    categorical_columns = data.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        st.write("Bar Chart")
        for col in categorical_columns:
            fig, ax = plt.subplots()
            data[col].value_counts().plot(kind="bar", ax=ax, color="orange")
            ax.set_title(f"Bar Chart of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            st.pyplot(fig)
    else:
        st.write("No categorical columns for bar charts.")

    # 3. Scatter plot between two numeric columns
    if len(numeric_columns) >= 2:
        st.write("Scatter Plot")
        col1 = st.selectbox("Select X-axis for Scatter Plot", numeric_columns)
        col2 = st.selectbox("Select Y-axis for Scatter Plot", numeric_columns)
        fig, ax = plt.subplots()
        ax.scatter(data[col1], data[col2], alpha=0.7, color="green")
        ax.set_title(f"Scatter Plot: {col1} vs {col2}")
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        st.pyplot(fig)
    else:
        st.write("Not enough numeric columns for scatter plot.")

    # 4. Pie chart for a categorical column
    if len(categorical_columns) > 0:
        st.write("Pie Chart")
        col = st.selectbox("Select a Column for Pie Chart", categorical_columns)
        fig, ax = plt.subplots()
        data[col].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%", colors=["lightblue", "pink", "lightgreen"])
        ax.set_title(f"Pie Chart of {col}")
        ax.set_ylabel("")  # Hide y-label for pie chart
        st.pyplot(fig)
    else:
        st.write("No categorical columns for pie chart.")

else:
    st.info("Please upload a CSV or Excel file to proceed.")
