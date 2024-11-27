import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("CSV File Viewer")

# File Upload Section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)
        
        # Display the dataframe
        st.subheader("Preview of the Uploaded CSV File")
        st.dataframe(data)  # Display as an interactive table
        
        # Display basic stats
        st.subheader("Basic Statistics")
        st.write(data.describe())
        
        # Option to download the uploaded file
        st.subheader("Download CSV Data")
        csv = data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="downloaded_data.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to view its contents.")
