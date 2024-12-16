import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set page layout
st.set_page_config(page_title="Dynamic Data Insights", layout="wide")

# Application Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Dynamic Data Insights Application</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #757575;'>Explore your data with customizable visualizations</h3>", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Load the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # File Info
        st.sidebar.write(f"**File Name:** {uploaded_file.name}")
        st.sidebar.write(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")

        # Dataset Preview
        st.markdown("### Dataset Preview")
        st.dataframe(df.head(), height=200)

        # Visualization Section
        st.markdown("## Generate Visualizations")
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found for visualizations.")
        else:
            col1, col2 = st.columns([2, 1])

            with col1:
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"],
                )

                if chart_type in ["Scatter Plot", "Line Chart"]:
                    x_col = st.selectbox("Select X-Axis Column", numeric_cols, key="x_axis")
                    y_col = st.selectbox("Select Y-Axis Column", numeric_cols, key="y_axis")
                else:
                    col = st.selectbox("Select Column", numeric_cols)

                # Color Palette Selection
                color_palette = st.color_picker("Pick a color for your chart", "#4CAF50")

                st.markdown("### Visualization")
                fig, ax = plt.subplots(figsize=(10, 6))

                # Generate Charts
                if chart_type == "Scatter Plot":
                    sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax, color=color_palette)
                    ax.set_title(f"Scatter Plot: {x_col} vs {y_col}", fontsize=14)
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                elif chart_type == "Line Chart":
                    ax.plot(df[x_col], df[y_col], color=color_palette)
                    ax.set_title(f"Line Chart: {x_col} vs {y_col}", fontsize=14)
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                elif chart_type == "Bar Chart":
                    df[col].value_counts().plot(kind="bar", ax=ax, color=color_palette)
                    ax.set_title(f"Bar Chart of {col}", fontsize=14)
                elif chart_type == "Histogram":
                    sns.histplot(df[col], ax=ax, kde=True, color=color_palette)
                    ax.set_title(f"Histogram of {col}", fontsize=14)
                elif chart_type == "Box Plot":
                    sns.boxplot(y=df[col], ax=ax, color=color_palette)
                    ax.set_title(f"Box Plot of {col}", fontsize=14)

                st.pyplot(fig)

                # Download Chart Option
                buffer = io.BytesIO()
                fig.savefig(buffer, format="png")
                st.download_button(label="Download Chart as PNG", data=buffer.getvalue(),
                                   file_name=f"{chart_type.lower()}_chart.png", mime="image/png")

            # Box for Dataset Summary
            with col2:
                st.markdown("<div style='background-color:#F0F8FF;padding:10px;border-radius:5px;'>"
                            "<h4 style='color:#4CAF50;'>Dataset Summary</h4>"
                            f"<p>Total Rows: <b>{df.shape[0]}</b></p>"
                            f"<p>Total Columns: <b>{df.shape[1]}</b></p>"
                            f"<p>Numeric Columns: <b>{', '.join(numeric_cols)}</b></p>"
                            "</div>", unsafe_allow_html=True)

            # Sidebar Dataset Download
            st.sidebar.subheader("📥 Download Dataset")
            download_buffer = io.BytesIO()
            df.to_csv(download_buffer, index=False)
            st.sidebar.download_button(label="Download Dataset as CSV", data=download_buffer.getvalue(),
                                        file_name="processed_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a file to proceed.")
