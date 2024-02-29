import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import plotly.figure_factory as ff



def main():
# Set page configuration for layout customization
    st.set_page_config(
        page_title="Analytics Dashboard",
        page_icon="📊",
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
if __name__ == "__main__":
    main()

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

st.markdown("<h1 style='text-align: left; color: black;'>Crop Recommendation Dashboard</h1>", unsafe_allow_html=True)

# NPK and THR Subplots
st.subheader("NPK and THR Charts")

selected_category = st.sidebar.selectbox("Select Category", ["All"] + list(categories.keys()))

# Filter data based on selected category
selected_plants = classified_plants.get(selected_category, plants)
selected_subcategory_plant = st.sidebar.selectbox("Select Subcategory Plant", selected_plants)

filtered_data = crop_data[crop_data['label'] == selected_subcategory_plant] if selected_category != "All" else crop_data

# Check if the DataFrame is not empty and contains the 'label' column before accessing it
if not filtered_data.empty and 'label' in filtered_data.columns:
    # NPK Pie Chart
    fig_npk = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

    avg_npk_values = filtered_data[['nitrogen_pmm', 'phosphorus_pmm', 'potassium_mm']].mean()
    values_npk = [avg_npk_values['nitrogen_pmm'], avg_npk_values['phosphorus_pmm'], avg_npk_values['potassium_mm']]

    fig_npk.add_trace(go.Pie(labels=['Nitrogen(N)', 'Phosphorous(P)', 'Potash(K)'], values=values_npk, hole=0,
                             marker=dict(colors=['red', 'blue', 'green'])), 1, 1)

    fig_npk.update_layout(title_text=f"Nitrogen, Phosphorus and Potassium Chart for {selected_subcategory_plant}")

    # THR Pie Chart
    fig_thr = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

    avg_thr_values = filtered_data[['temperature_f', 'humidity', 'rainfall_mm']].mean()
    values_thr = [avg_thr_values['temperature_f'], avg_thr_values['humidity'], avg_thr_values['rainfall_mm']]

    fig_thr.add_trace(go.Pie(labels=['Temperature', 'Humidity', 'Rainfall'], values=values_thr, hole=0,
                             marker=dict(colors=['red', 'blue', 'green'])), 1, 1)

    fig_thr.update_layout(title_text=f"Temperature, Humidity and Rainfall Chart for {selected_subcategory_plant}")

    # Display the NPK and THR pie charts
    st.plotly_chart(fig_npk)
    st.plotly_chart(fig_thr)

    # Line Chart for Temperature, Humidity, and Rainfall
    st.subheader("Line Chart for Temperature, Humidity, and Rainfall")
    line_chart_data = crop_data[crop_data['label'] == selected_subcategory_plant] if selected_category != "All" else crop_data

    fig_line_chart = go.Figure()

    # Adding traces for Temperature, Humidity, and Rainfall
    fig_line_chart.add_trace(go.Scatter(x=line_chart_data.index, y=line_chart_data['temperature_f'],
                                        mode='lines', name='Temperature', line=dict(color='red')))
    fig_line_chart.add_trace(go.Scatter(x=line_chart_data.index, y=line_chart_data['humidity'],
                                        mode='lines', name='Humidity', line=dict(color='blue')))
    fig_line_chart.add_trace(go.Scatter(x=line_chart_data.index, y=line_chart_data['rainfall_mm'],
                                        mode='lines', name='Rainfall', line=dict(color='green')))

    fig_line_chart.update_layout(title=f"Temperature, Humidity, and Rainfall Trends for {selected_subcategory_plant}",
                                 xaxis_title="Index", yaxis_title="Values")

    st.plotly_chart(fig_line_chart)

    
    # Pair Plot
    st.subheader("Pair Plot")
    selected_features = ["temperature_f", "humidity", "rainfall_mm", "nitrogen_pmm", "phosphorus_pmm", "potassium_mm", "label"]
    pair_plot_data = crop_data[selected_features]

    # Filter data based on selected category for pair plot
    pair_plot_data_category = pair_plot_data[pair_plot_data['label'] == selected_subcategory_plant] if selected_category != "All" else pair_plot_data


    # Set the style and color palette if needed
    sns.set_theme(style="ticks")
    colors = sns.color_palette("husl")
    # Custom function to create pair plot on a specific axes
    def create_pair_plot(data, hue, palette, figsize):
        pair_plot = sns.pairplot(data, hue=hue, palette=palette, height=figsize[1])
        pair_plot.figure.suptitle(f"Pair Plot for {selected_subcategory_plant}", y=1.02)
        return pair_plot
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(12, 8))
    pair_plot = create_pair_plot(pair_plot_data_category, 'label', colors, figsize=(12, 8))
    st.pyplot(fig=pair_plot.figure, dpi=fig.dpi, clear_figure=True)


    # # Seaborn Pair Plot
    # plt.figure(figsize=(12, 8))
    # pair_plot = sns.pairplot(pair_plot_data_category, hue='label', palette=colors)
    # pair_plot.figure.suptitle(f"Pair Plot for {selected_subcategory_plant}", y=1.02)
    # st.pyplot(fig.dpi, clear_figure=True)

    # Correlation Matrix
    st.subheader("Correlation Matrix")
    correlation_data = pair_plot_data_category.drop(columns=['label'])  # Exclude 'label' for correlation matrix
    correlation_matrix = correlation_data.corr()

    # Plotting the correlation matrix as a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title(f"Correlation Matrix for {selected_subcategory_plant}")
    st.pyplot()
