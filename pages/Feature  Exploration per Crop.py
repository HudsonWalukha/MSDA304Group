import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import random
import plotly.express as px

# Set page configuration for layout customization
st.set_page_config(
    page_title="Feature vs Crop Distribution",
    page_icon="📉",  
    layout="centered",  # Center the app on the screen
    initial_sidebar_state="auto",
)

# Set theme and layout customization
st.markdown(
    """
    <style>
    .css-1v3fvcr {  # Customize the font size and color
        font-size: 20px;
        color: #2b2b2b;
    }
    body {
        background-image: url('crop1.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Load your crop recommendation data
data = pd.read_csv('./data/304_dataset.csv')
def clean_crop_data(df):
    """Cleans and prepares crop data for analysis.
    Args: pd.DataFrame crop data to be cleaned.
    Returns: The cleaned crop data.
    """
    # Clean column names
    # remove brackets
    df.columns = [col.lower().strip().replace('(', ' ').replace(')', '') for col in df.columns]

    # replace whitespace with underscores
    df.columns = [col.replace(' ', "_") for col in df.columns]
    # Drop null values
    df.dropna(inplace=True)

    # Round specified columns to 4 decimal places
    for col in ['temperature_f', 'humidity', 'soil_ph', 'rainfall_mm']:
        df[col] = df[col].round(4)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Drop records with label "mungbean"
    df = df.query('label != "mungbean"')
    return df

# Applying the data cleaning function
crop_data = clean_crop_data(data)

# Custom colors for each crop
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Plant Category Code
plants = ['Carrots', 'onions', 'pomegranate', 'rice', 'greengram', 'lentil', 'mango', 'chickpea', 'coffee', 'papaya',
          'pigeonpeas', 'apple', 'maize', 'banana', 'kidneybeans', 'coconut', 'grapes', 'cotton',
          'lettuce', 'tomato', 'Cabbage', 'watermelon', 'orange']

# Define categories and corresponding plants
categories = {
    "vegetables": ["Carrots", "onions", "lettuce", "tomato", "Cabbage"],
    "cereals": ["rice", "maize"],
    "fruits": ["pomegranate", "mango", "apple", "papaya", "banana", "grapes", "orange"],
    "legumes": ["greengram", "lentil", "chickpea", "pigeonpeas", "kidneybeans", "mungbean"],
    "others": ["coffee", "coconut", "cotton"]
}

# Classify plants into categories
classified_plants = {category: [plant for plant in plants if plant in plant_list] for category, plant_list in categories.items()}
# Assuming crop_average is your DataFrame containing nitrogen and other features
# ...
crop_average = pd.pivot_table(data,index=['label'],aggfunc='mean').round(2)
# Create and sort DataFrame
nitrogen_summary = crop_average.sort_values(by='nitrogen_pmm', ascending=False)




# Streamlit app
st.title("Feature Requirements per Crop Dashboard")

# Feature selection dropdown
selected_feature = st.selectbox("Select Feature", list(nitrogen_summary.columns))

# Filter data based on selected feature
selected_summary = nitrogen_summary.sort_values(by=selected_feature, ascending=False)

# Create subplots
fig = make_subplots(rows=1, cols=2)

# Define data for subplots
top = selected_summary.head(10)
last = selected_summary.tail(10)

# Generate unique color palettes for top and last
color_palette_top = px.colors.qualitative.Set1
color_palette_last = px.colors.qualitative.Set2

# Add bar traces to subplots
fig.add_trace(
    go.Bar(
        y=top.index,
        x=top[selected_feature],
        name=f"{selected_feature} Intensive Crops",
        marker_color=random.choice(color_palette_top),
        orientation='h',
        text=top[selected_feature]
    ), row=1, col=1)

fig.add_trace(
    go.Bar(
        y=last.index,
        x=last[selected_feature],
        name=f"Less {selected_feature} Intensive Crops",
        marker_color=random.choice(color_palette_last),
        orientation='h',
        text=last[selected_feature]
    ), row=1, col=2)

# Update trace settings and layout
fig.update_traces(texttemplate='%{text}', textposition='inside')
fig.update_layout(
    title_text=f"{selected_feature} Requirements per Crop",
    plot_bgcolor='white',
    font_size=12,
    font_color='black',
    height=500,
    width=1000  # Set the width to 800 pixels (adjust as needed)
)

# Update axes and display the figure
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

# Display the figure using st.plotly_chart
st.plotly_chart(fig)
