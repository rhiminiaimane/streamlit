import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# set page configutation

st.set_page_config(page_title="Data Visualisation",
                   layout="centered",
                   page_icon="📊")

# title

st.title("📊 Data Visualisation - Web App")

# geting the working directry

working_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = f"{working_dir}/data"

# list the files present in data folder

files = []

for f in os.listdir(folder_path):
    if f.endswith(".csv"):
        files.append(f)

# dropdown for all the files

selected_file = st.selectbox("Select a file", files, index = None)
if selected_file :
    # get the path of the selected file
    file_path = os.path.join(folder_path, selected_file)

    # reading the csv file as a pandas dataFrame
    df = pd.read_csv(file_path)


    st.write("")
    st.write(df.head(5))

    col1, col2= st.columns(2)
    columns = df.columns.tolist()

    with col1:
        x_axis = st.selectbox("Select the X axis", options=columns + ["None"], index=None)
        plot_list = ["Line Plot", "Bar Chart", "Scatter Plot", "Distribution Plot", "Count Plot"]

        selected_plot = st.selectbox("Select a plot", options=plot_list)

    with col2:
        # user selection of columns 
        y_axis = st.selectbox("Select the Y axis", options=columns + ["None"], index=None)
        

    if st.button("Generate Plot"):
        fig, ax = plt.subplots(figsize=(6, 4))

        if selected_plot == "Line Plot":
            sns.lineplot(x = df[x_axis], y = df[y_axis], ax = ax)
        
        elif selected_plot == "Bar Chart":
            sns.barplot(x = df[x_axis], y = df[y_axis], ax = ax)

        elif selected_plot == "Scatter Plot":
            sns.scatterplot(x = df[x_axis], y = df[y_axis], ax = ax)

        elif selected_plot == "Distribution Plot":
            sns.histplot(df[x_axis], kde=True, ax=ax)

        elif selected_plot == "Count Plot":
            sns.countplot(df[x_axis], ax=ax)
            y_axis = 'Count'

        
        # adjust label sizes

        ax.tick_params(axis = "x", labelsize=10)
        ax.tick_params(axis = "y", labelsize=10)

        # title axis labels

        plt.title(f"{selected_plot} of {y_axis} vs {x_axis}", fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        st.pyplot(fig)