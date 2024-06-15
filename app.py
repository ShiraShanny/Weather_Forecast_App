import streamlit as st
import datetime as dt
import pytz
from timezonefinder import TimezoneFinder
import requests
import base64
from Main import encode_api_key

def get_weather_data(encoded_key, city_name, state_code = '', country_code = '',units = 'F'):
  if units == 'C':
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={base64.b64decode(encoded_key).decode('utf-8')}&units=metric"""
  else:
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={base64.b64decode(encoded_key).decode('utf-8')}&units=imperial"""
  response = requests.get(url)
  return response.json()

# Main function for the Streamlit app
def weather_checker_app():
    st.title('Weather Checker App')
    st.subheader('This app presents the weather and time in your desired location')

    API_key = 'b03f17721ddcc0700bb0dcc4b47d5dbf'
    encoded_key = encode_api_key(API_key)
    city_name = st.text_input('Enter city name:', 'New York')
    state_code = st.text_input('Enter State code (optional):')
    country_code = st.text_input('Enter Country code (optional):').upper()
    units = st.text_input('Enter temperature units (C/F): ', 'F').upper()

    if st.button('Get Weather'):
        try:
            weather_data = get_weather_data(encoded_key, city_name, state_code, country_code, units)
            if weather_data["cod"] == 200:
                st.write(f"Weather in {city_name}, {country_code}: {weather_data['weather'][0]['description']}")
                st.write(f"Temperature: {weather_data['main']['temp']}°{units}")
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