import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
import openai  # Example for connecting LLM, replace with your LLM of choice

# OpenAI setup (replace with your key if using OpenAI)
openai.api_key = "your-api-key"  # Use your key if connecting to OpenAI or other LLMs

# Streamlit App Title
st.title("Automated Data Analysis and Dashboard Generation")

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

    # Step 1: Check for null values
    if data.isnull().sum().sum() > 0:
        st.warning("Your dataset contains missing values.")
        st.write(data.isnull().sum())

        # User input for handling null values
        null_option = st.radio(
            "How would you like to handle the missing values?",
            ("Remove rows with missing values", "Impute missing values"),
        )

        if null_option == "Remove rows with missing values":
            data = data.dropna()
            st.success("Missing values removed.")
        else:
            # Imputation options
            st.info("Choose imputation method based on column type.")
            numeric_strategy = st.selectbox(
                "Numeric columns imputation method", ["Mean", "Median", "Most Frequent"]
            )
            categorical_strategy = st.selectbox(
                "Categorical columns imputation method", ["Most Frequent", "Constant"]
            )

            # Impute numeric columns
            if numeric_strategy:
                num_imputer = SimpleImputer(strategy=numeric_strategy.lower())
                numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
                data[numeric_cols] = num_imputer.fit_transform(data[numeric_cols])

            # Impute categorical columns
            if categorical_strategy:
                cat_imputer = SimpleImputer(
                    strategy="most_frequent"
                    if categorical_strategy == "Most Frequent"
                    else "constant",
                    fill_value="Missing",
                )
                cat_cols = data.select_dtypes(include=['object']).columns
                data[cat_cols] = cat_imputer.fit_transform(data[cat_cols])

            st.success("Missing values imputed.")

    st.subheader("Cleaned Data")
    st.write(data.head())

    # Step 2: User Input for Dashboard Requirements
    st.subheader("Build Your Dashboard")
    graph_options = st.multiselect(
        "Choose the types of graphs you want in your dashboard",
        ["Histogram", "Bar Chart", "Scatter Plot", "Line Plot", "Pie Chart"],
    )

    # Generate graphs
    st.subheader("Dashboard")
    for graph in graph_options:
        if graph == "Histogram":
            col = st.selectbox("Select a numeric column for Histogram", data.select_dtypes(include=['float64', 'int64']).columns)
            fig, ax = plt.subplots()
            ax.hist(data[col], bins=20, color='skyblue')
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)

        elif graph == "Bar Chart":
            col = st.selectbox("Select a categorical column for Bar Chart", data.select_dtypes(include=['object']).columns)
            fig, ax = plt.subplots()
            data[col].value_counts().plot(kind="bar", ax=ax, color="orange")
            ax.set_title(f"Bar Chart of {col}")
            st.pyplot(fig)

        elif graph == "Scatter Plot":
            numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
            col_x = st.selectbox("Select X-axis for Scatter Plot", numeric_cols)
            col_y = st.selectbox("Select Y-axis for Scatter Plot", numeric_cols)
            fig, ax = plt.subplots()
            ax.scatter(data[col_x], data[col_y], alpha=0.7, color="green")
            ax.set_title(f"Scatter Plot: {col_x} vs {col_y}")
            st.pyplot(fig)

        elif graph == "Line Plot":
            numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
            col_x = st.selectbox("Select X-axis for Line Plot", numeric_cols)
            col_y = st.selectbox("Select Y-axis for Line Plot", numeric_cols)
            fig, ax = plt.subplots()
            ax.plot(data[col_x], data[col_y], color="blue")
            ax.set_title(f"Line Plot: {col_x} vs {col_y}")
            st.pyplot(fig)

        elif graph == "Pie Chart":
            col = st.selectbox("Select a categorical column for Pie Chart", data.select_dtypes(include=['object']).columns)
            fig, ax = plt.subplots()
            data[col].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")
            ax.set_title(f"Pie Chart of {col}")
            st.pyplot(fig)

    # Optional: Use LLM for assistance
    st.subheader("Ask the Model for Insights")
    user_query = st.text_input("Enter your question about the dataset:")
    if user_query:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Analyze the dataset and answer this question: {user_query}",
                max_tokens=100,
            )
            st.write("Model's Response:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error interacting with the model: {e}")
else:
    st.info("Please upload a CSV or Excel file to proceed.")
