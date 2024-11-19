import os
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Cleaning", layout="centered", page_icon="📊")

st.title("🧹 Data Cleaning - Web App")

st.sidebar.markdown("<h1 style='text-align: center;'>Data Lab</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: left;'>Upload data</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Initialize session state variables
if 'original_df' not in st.session_state:
    st.session_state['original_df'] = None

if 'working_df' not in st.session_state:
    st.session_state['working_df'] = None

if uploaded_file is not None:
    # Load the uploaded file into the original dataset
    if st.session_state['original_df'] is None:
        df = pd.read_csv(uploaded_file)
        st.session_state['original_df'] = df

    st.write("You uploaded a file:")
    st.write("### Dataset Preview :")
    pd.set_option('display.max_rows', None)
    st.dataframe(st.session_state['original_df'])
    st.write("Shape of the Uploaded Dataset:", st.session_state['original_df'].shape[0], "rows and ", st.session_state['original_df'].shape[1], "columns.")

else:
    st.write("Please upload a CSV file.")

if st.session_state['original_df'] is not None:
    st.sidebar.markdown("<h3>Remove Columns</h3>", unsafe_allow_html=True)
    
    # Select columns to remove from the working dataset
    if st.session_state['working_df'] is not None:
        columns_to_remove = st.sidebar.multiselect("Select columns to remove", st.session_state['working_df'].columns)
    else:
        columns_to_remove = st.sidebar.multiselect("Select columns to remove", st.session_state['original_df'].columns)
    
    if st.sidebar.button("Delete Columns"):
        if columns_to_remove:
            # Create the working dataset from the original if it doesn't exist
            if st.session_state['working_df'] is None:
                st.session_state['working_df'] = st.session_state['original_df'].copy()

            # Remove selected columns
            st.session_state['working_df'] = st.session_state['working_df'].drop(columns=columns_to_remove)
            st.write(f"Removed columns: {', '.join(columns_to_remove)}")
            st.write("### Updated Working Dataset:")
            st.dataframe(st.session_state['working_df'])
        else:
            st.write("No columns were selected for removal.")

# Encoding functionality moved to the sidebar
if st.session_state['working_df'] is not None:
    st.sidebar.markdown("<h3>Encode Columns</h3>", unsafe_allow_html=True)
    column_to_encode = st.sidebar.selectbox("Select column to encode", [""] + list(st.session_state['working_df'].columns))
    if column_to_encode:
        unique_values = st.session_state['working_df'][column_to_encode].unique()
        st.sidebar.write(f"Unique values in {column_to_encode}: {unique_values}")
        if st.sidebar.button("Encode Selected Column"):
            encoder = LabelEncoder()
            original_values = st.session_state['working_df'][column_to_encode].copy()
            st.session_state['working_df'][column_to_encode] = encoder.fit_transform(st.session_state['working_df'][column_to_encode])
            encoding_mapping = pd.DataFrame({
                'Old Value': original_values.unique(),
                'New Value': encoder.transform(original_values.unique())
            })
            st.write(f"Encoding for {column_to_encode}:")
            st.write(encoding_mapping)

# Data type correction functionality
if st.session_state['working_df'] is not None:
    st.sidebar.markdown("<h3>Change Column Data Type</h3>", unsafe_allow_html=True)
    
    # Select a column to change data type
    column_to_change = st.sidebar.selectbox("Select column to change type", [""] + list(st.session_state['working_df'].columns))
    
    if column_to_change:
        # Select the target data type
        data_types = ['int', 'float', 'str', 'datetime']
        new_data_type = st.sidebar.selectbox("Select new data type", data_types)
        
        if st.sidebar.button("Change Data Type"):
            try:
                if new_data_type == 'int':
                    st.session_state['working_df'][column_to_change] = st.session_state['working_df'][column_to_change].astype(int)
                elif new_data_type == 'float':
                    st.session_state['working_df'][column_to_change] = st.session_state['working_df'][column_to_change].astype(float)
                elif new_data_type == 'str':
                    st.session_state['working_df'][column_to_change] = st.session_state['working_df'][column_to_change].astype(str)
                elif new_data_type == 'datetime':
                    st.session_state['working_df'][column_to_change] = pd.to_datetime(st.session_state['working_df'][column_to_change], errors='coerce')
                
                st.write(f"Data type of column '{column_to_change}' changed to {new_data_type}.")
                st.write("### Updated Working Dataset:")
                st.dataframe(st.session_state['working_df'])
            except Exception as e:
                st.write(f"Error changing data type for column '{column_to_change}': {e}")

if st.session_state['working_df'] is not None:
    if st.button("Generate Correlation Matrix"):
        st.write("### Correlation Matrix")
        correlation_matrix = st.session_state['working_df'].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
        st.pyplot(plt)
        st.write("### Identifying Highly Correlated Columns:")
        threshold = 0.8
        corr_pairs = correlation_matrix.unstack().sort_values(ascending=False)
        highly_correlated = corr_pairs[(corr_pairs > threshold) & (corr_pairs < 1)]
        if not highly_correlated.empty:
            st.write("Highly correlated column pairs (correlation > 0.8):")
            st.write(highly_correlated)
        else:
            st.write("No highly correlated column pairs detected.")

if st.session_state['working_df'] is not None:
    if st.button("Start Cleaning"):
        total_nan_values = st.session_state['working_df'].isna().sum().sum()
        num_duplicates = st.session_state['working_df'].duplicated().sum()
        st.session_state['working_df'] = st.session_state['working_df'].drop_duplicates()
        st.session_state['working_df'] = st.session_state['working_df'].dropna()
        st.write(f"Your dataset contains: {total_nan_values} NaN values and {num_duplicates} duplicate rows!")
        st.write("Cleaned Dataset:")
        st.dataframe(st.session_state['working_df'])
        st.write("New Shape of the Dataset (after cleaning):", st.session_state['working_df'].shape)