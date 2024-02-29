import pickle
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the model in Keras format
model = load_model('Intelligent_Crop_Selector')
#load the pickled label encoder for one-hot encoding
with open('label_encoder.pkl', 'rb') as label_encoder_file:
    label_encoder = pickle.load(label_encoder_file)
# Load the scaler for standardizing input features
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall):
    try:
        # Create a numpy array from the user input
        input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]])

        # Standardize the input features using the loaded scaler
        input_data_scaled = scaler.transform(input_data)

        # Use the model to make a prediction
        prediction = model.predict(input_data_scaled)

        return prediction[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

def decode_one_hot(prediction):
    # Assuming prediction is a one-hot encoded array
    predicted_class = np.argmax(prediction)
    return predicted_class



def main():
# Set page configuration for layout customization
    st.set_page_config(
        page_title="Intelligent Crop Selector",
        page_icon="🌾",
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

    st.title("Intelligent Crop Selector")

    # User input for parameters
    nitrogen = st.number_input("Nitrogen (pmm)")
    phosphorus = st.number_input("Phosphorus (pmm)")
    potassium = st.number_input("Potassium (pmm)")
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    soil_ph = st.number_input("Soil pH")
    rainfall = st.number_input("Rainfall (mm)")

    if st.button("Predict Crop"):
        # Validate that all input values are non-default
        if all([nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]):
            crop_prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall)

            if crop_prediction is not None:
                try:
                    # Decode one-hot encoded prediction
                    predicted_class = decode_one_hot(crop_prediction)

                    # Decode the predicted class to crop name using label encoder
                    predicted_crop = label_encoder[predicted_class]

                    st.success(f"The recommended crop for the climatic condition is: {predicted_crop}")
                except Exception as e:
                    st.error(f"Error during label decoding: {e}")
        else:
            st.warning("Please enter non-default values for all parameters.")

if __name__ == "__main__":
    main()