import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium
'''
# SPACE TRAVEL TAXI CO.
'''
st.markdown(f'''
We are a space travel company,
Please provide your location and destination.
We will warp a vessel toward your destination as soon as possible.
\n
### WARNING
_Make sure to hold on to your wig, the wormholes opening, could suck it in_
''')
pickup_date = st.date_input("Pickup Date", value=datetime.now().date())
pickup_time = st.time_input("Pickup Time", value=datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time).strftime("%Y-%m-%d %H:%M:%S")

# Default coordinates

pickup_longitude = -73.985428
pickup_latitude = 40.748817
dropoff_longitude = -73.985428
dropoff_latitude = 40.748817

# Buttons to choose pickup and dropoff locations

if st.button("Choose Pickup Location"):
    st.session_state['choose_location'] = 'pickup'
if st.button("Choose Dropoff Location"):
    st.session_state['choose_location'] = 'dropoff'

# Update coordinates based on map click

if 'choose_location' in st.session_state:
    if 'last_clicked' in st.session_state:
        if st.session_state['choose_location'] == 'pickup':
            pickup_longitude, pickup_latitude = st.session_state['last_clicked']
        elif st.session_state['choose_location'] == 'dropoff':
            dropoff_longitude, dropoff_latitude = st.session_state['last_clicked']
        del st.session_state['choose_location']
        del st.session_state['last_clicked']

# Create a map centered around the default pickup location
m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=15)

# Add markers for pickup and dropoff locations

pickup_marker = folium.Marker([pickup_latitude, pickup_longitude], popup="Pickup Location", icon=folium.Icon(color="green"))
dropoff_marker = folium.Marker([dropoff_latitude, dropoff_longitude], popup="Dropoff Location", icon=folium.Icon(color="red"))
pickup_marker.add_to(m)
dropoff_marker.add_to(m)

# Display the map
map_data = st_folium(m, width=700, height=500)

# Update coordinates based on map click

if map_data['last_clicked']:
    if 'choose_location' in st.session_state:
        if st.session_state['choose_location'] == 'pickup':
            pickup_longitude, pickup_latitude = map_data['last_clicked']['lng'], map_data['last_clicked']['lat']
        elif st.session_state['choose_location'] == 'dropoff':
            dropoff_longitude, dropoff_latitude = map_data['last_clicked']['lng'], map_data['last_clicked']['lat']
        del st.session_state['choose_location']

# Display updated coordinates in input fields

st.number_input("Pickup Longitude", value=pickup_longitude, key="pickup_longitude")
st.number_input("Pickup Latitude", value=pickup_latitude, key="pickup_latitude")
st.number_input("Dropoff Longitude", value=dropoff_longitude, key="dropoff_longitude")
st.number_input("Dropoff Latitude", value=dropoff_latitude, key="dropoff_latitude")
passenger_count = st.number_input("Number of Passengers", min_value=1, max_value=6, value=1)

url = 'https://taxifare.lewagon.ai/predict'
if st.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }
    response = requests.get(url, params=params)
    prediction = response.json().get("fare", "Error")
    st.markdown(f"##  Fare: ${prediction:.2f}")
