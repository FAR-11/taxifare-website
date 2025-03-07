import streamlit as st
import requests

# Page title
st.title("Taxi Fare Prediction")

st.markdown("### Enter your ride details")

# User input fields
pickup_datetime = st.text_input("Date & Time (YYYY-MM-DD HH:MM:SS)")
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Number of Passengers", min_value=1, max_value=6, value=1)

# API URL
url = "https://taxifare.lewagon.ai/predict"

# Button to trigger prediction
if st.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }

    # API request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get("fare", "Error")
        st.success(f"Estimated Fare: ${prediction:.2f}")
    else:
        st.error("Error fetching the prediction. Please check your input.")
