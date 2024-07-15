import streamlit as st
import pandas as pd
import plotly.express as px

# Function to read uploaded file
@st.cache(allow_output_mutation=True)
def load_data(file):
    try:
        df = pd.read_excel(file)
    except Exception as e:
        print(e)
        df = None
    return df

# Read the default COVID-19 data from Excel file
default_file_path = r"C:\Users\eastm\Documents\Pyprojects\Dataviz_project\data\COVID-19-geographic-disbtribution-worldwide.xlsx"
default_data = pd.read_excel(default_file_path)

# Convert dateRep to datetime
default_data['dateRep'] = pd.to_datetime(default_data['dateRep'])

# Sidebar for file upload and filtering options
st.sidebar.header('Upload New Data')
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xlsx'])

# Initialize data variable
data = default_data.copy()

# If file is uploaded, load new data and show basic statistics
if uploaded_file is not None:
    new_data = load_data(uploaded_file)
    if new_data is not None:
        st.subheader('New Data - Raw Data')
        st.write(new_data.head())

        # Convert dateRep to datetime
        if 'dateRep' in new_data.columns:
            new_data['dateRep'] = pd.to_datetime(new_data['dateRep'])

        # Update data variable to new dataset
        data = new_data.copy()

    else:
        st.write("Invalid file format. Please upload an Excel file.")

# Show default dataset statistics
st.subheader('Default Data - Raw Data')
st.write(default_data.head())

# Convert dateRep to datetime
if 'dateRep' in data.columns:
    data['dateRep'] = pd.to_datetime(data['dateRep'])

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Convert start_date and end_date to pandas Timestamp objects
start_date = pd.Timestamp(st.sidebar.date_input("Start Date", data['dateRep'].min()))
end_date = pd.Timestamp(st.sidebar.date_input("End Date", data['dateRep'].max()))

# Filter data based on selected date range
filtered_data = data[(data['dateRep'] >= start_date) & (data['dateRep'] <= end_date)]

# Download button for raw data
st.subheader('Download Raw Data')
st.write("Click below to download the raw data.")
st.download_button(
    label="Download CSV",
    data=filtered_data.to_csv().encode('utf-8'),
    file_name='covid_data.csv',
    mime='text/csv'
)

# Display charts and map side by side
st.subheader('Charts Overview')

# Chart 1: Line chart for daily cases
st.subheader('Daily Cases')
daily_cases = filtered_data.groupby('dateRep')['cases'].sum()
st.line_chart(daily_cases, width=0.5)  # Adjust width as needed

# Chart 2: Bar chart for monthly cases
st.subheader('Monthly Cases')
monthly_cases = filtered_data.groupby(filtered_data['dateRep'].dt.to_period('M'))['cases'].sum()
st.bar_chart(monthly_cases, width=0.5)  # Adjust width as needed

# Map visualization for cases by country
st.subheader('Map Visualization')

# Aggregate data by country for map visualization
country_data = filtered_data.groupby('countriesAndTerritories', as_index=False)['cases'].sum()

# Plotly map visualization
fig = px.choropleth(country_data,
                    locations="countriesAndTerritories",
                    locationmode="country names",
                    color="cases",
                    hover_name="countriesAndTerritories",
                    title="COVID-19 Cases by Country",
                    color_continuous_scale=px.colors.sequential.Plasma)

st.plotly_chart(fig, use_container_width=True)  # Use container width for full-width display
