import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 CSV Dashboard")

uploaded = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded is not None:
    st.success("File uploaded successfully")
    df = pd.read_csv(uploaded)

    st.write("Preview of Dataset:")
    st.dataframe(df)

    
    st.sidebar.title('Options for Data Cleaning')

    if st.sidebar.button("Drop Null"):
        df.dropna(inplace=True)
        st.write("✅ Removed null values")

    if st.sidebar.button("Remove Duplicates"):
        df.drop_duplicates(inplace=True)
        st.write("✅ Removed duplicates")

   
    missing_cols = df.isnull().sum()
    st.write("🔍 Missing values in each column:")
    st.write(missing_cols[missing_cols > 0])

    st.write("🧾 Columns with missing values:")
    st.write(missing_cols)

    if not missing_cols[missing_cols > 0].empty:
        selected_col = st.selectbox("Select a column to fill missing values:", missing_cols.index)

        fill_method = st.radio("Choose a method to fill missing values:",
                            ("Fill with 0", "Fill with Mean", "Fill with Median", "Fill with Mode", "Fill with 'Missing'"))

        if st.button("Fill Missing Values"):
            if fill_method == "Fill with 0":
                df[selected_col].fillna(0, inplace=True)
            elif fill_method == "Fill with Mean":
                if pd.api.types.is_numeric_dtype(df[selected_col]):
                    df[selected_col].fillna(df[selected_col].mean(), inplace=True)
                else:
                    st.warning("Mean can only be applied to numeric columns.")
            elif fill_method == "Fill with Median":
                if pd.api.types.is_numeric_dtype(df[selected_col]):
                    df[selected_col].fillna(df[selected_col].median(), inplace=True)
                else:
                    st.warning("Median can only be applied to numeric columns.")
            elif fill_method == "Fill with Mode":
                mode_val = df[selected_col].mode()
                if not mode_val.empty:
                    df[selected_col].fillna(mode_val[0], inplace=True)
            elif fill_method == "Fill with 'Missing'":
                df[selected_col].fillna("Missing", inplace=True)

    st.subheader("Updated DataFrame:")
    st.dataframe(df)

   
    st.sidebar.title("📈 Plot Options")

    all_cols = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    plot_type = st.sidebar.selectbox("Select Plot Type", 
                                    ["Line Plot", "Bar Plot", "Scatter Plot", "Box Plot", "Histogram"])
    
    x_col = st.selectbox("Select X-axis", all_cols)
    y_col = st.selectbox("Select Y-axis", all_cols)

    st.write(f"### {plot_type}")

    fig, ax = plt.subplots()

    if plot_type == "Line Plot":
        ax.plot(df[x_col], df[y_col])
    elif plot_type == "Bar Plot":
        ax.bar(df[x_col], df[y_col])
    elif plot_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    elif plot_type == "Box Plot":
        sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
    elif plot_type == "Histogram":
        sns.histplot(data=df, x=x_col, ax=ax)

    st.pyplot(fig)

else:
    st.warning("📁 Please upload a CSV file to get started.")




    
# python -m streamlit run dashboard.py
