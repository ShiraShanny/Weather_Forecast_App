import streamlit as st
import datetime as dt
import pytz
from timezonefinder import TimezoneFinder
from collections import Counter
import requests
import json


# Load city list
def load_city_list(file_path):
    with open(file_path, encoding="utf8") as file:
        city_list = json.load(file)
    return city_list


# Find duplicate city names
def find_duplicate_cities(city_list):
    city_names = [entry['name'].lower() for entry in city_list]
    city_count = Counter(city_names)
    duplicate_cities = [name for name, count in city_count.items() if count > 1]
    return duplicate_cities


# Get weather data from OpenWeatherMap API
def get_weather_data(city_name, state_code, country_code, duplicate_cities, API_key):
    if city_name.lower() in duplicate_cities:
        if state_code.lower() != 'na':
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={API_key}&units=metric"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"

    response = requests.get(url)
    return response.json()


# Main function for the Streamlit app
def weather_checker_app():
    st.title('Weather Checker App')
    st.subheader('This app presents the weather and time in your desired location')

    API_key = 'ec45812d74648049b38512b286f1ae6d'
    city_name = st.text_input('Enter city name:', 'New York')
    state_code = st.text_input('Enter State code:')
    country_code = st.text_input('Enter Country code:')

    city_list = load_city_list('city.list.json')
    duplicate_cities = find_duplicate_cities(city_list)

    if st.button('Get Weather'):
        try:
            weather_data = get_weather_data(city_name, state_code, country_code, duplicate_cities, API_key)
            if weather_data["cod"] == 200:
                st.write(f"Weather in {city_name}: {weather_data['weather'][0]['description']}")
                st.write(f"Temperature: {weather_data['main']['temp']}°C")
                st.write(f"Humidity: {weather_data['main']['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

                coord = weather_data['coord']
                latitude = coord['lat']
                longitude = coord['lon']

                tf = TimezoneFinder()
                city_timezone = tf.timezone_at(lng=longitude, lat=latitude)
                city_tz = pytz.timezone(city_timezone)
                utc_now = dt.datetime.now(pytz.utc)
                city_time = utc_now.astimezone(city_tz)

                st.write(f"Local time: {city_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            else:
                st.write("City not found. Please check the city name.")
        except Exception as e:
            st.write(f"An error occurred: {e}")


if __name__ == "__main__":
    weather_checker_app()