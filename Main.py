import json
import datetime as dt
import pytz
from timezonefinder import TimezoneFinder
import requests
import base64

def get_weather_data(encoded_key, city_name, state_code = '', country_code = '',units = 'F'):
  if units == 'C':
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={base64.b64decode(encoded_key).decode('utf-8')}&units=metric"""
  else:
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={base64.b64decode(encoded_key).decode('utf-8')}&units=imperial"""
  response = requests.get(url)
  return response

def encode_api_key(API_key):
    encoded_key = base64.b64encode(API_key.encode()).decode('utf-8')
    return encoded_key

API_key = 'b03f17721ddcc0700bb0dcc4b47d5dbf'
encoded_key = encode_api_key(API_key)

def city_timezone(latitude, longitude):
  tf = TimezoneFinder()
  city_timezone = tf.timezone_at(lng=longitude, lat=latitude)
  city_tz = pytz.timezone(city_timezone)
  utc_now = dt.datetime.now(pytz.utc)
  city_time = utc_now.astimezone(city_tz)
  return city_time

def load_settings(file_path):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {}
    return settings

def save_settings(file_path, settings):
    with open(file_path, 'w') as file:
        json.dump(settings, file, indent=4)

def main():

    while True:
        settings = load_settings('settings.json')
        print("\nMenu:")
        print("1. Set default city")
        print("2. Add favorite city")
        print("3. Fetch weather")
        print("4. Fetch weather of favorite city")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            city_name = input("Enter the default city name: ").lower()
            state_code = input("Enter state code(or leave empty): ")
            country_code = input("Enter country code(or leave empty): ")
            settings['default_city']={}
            settings['default_city'].update({city_name:{'city_name':city_name, 'state_code':state_code, 'country_code':country_code}})
            settings['state_code'] = state_code
            settings['country_code'] = country_code
            save_settings('settings.json', settings)
            print(f"Default city set to: {city_name}")
        elif choice == '2':
            favorite_city = input("Enter the city name to add to favorites: ").lower()
            favorite_state_code = input("Enter state code(or leave empty): ")
            favorite_country_code = input("Enter country code(or leave empty): ")
            if "favorite_cities" not in settings:
              settings['favorite_cities'] = {}
            settings['favorite_cities'].update({favorite_city:{'city_name':favorite_city,'state_code':favorite_state_code,'country_code':favorite_country_code}})
            save_settings('settings.json', settings)
            print(f"{favorite_city} added to favorite cities.")
        elif choice == '3':
            city_name = input("Enter the city name (or leave blank to use default): ").lower()
            state_code = input("Enter state code(or leave empty): ")
            country_code = input("Enter country code(or leave empty): ")
            units = input("Enter temperature units (C/F): ").upper()
            if not city_name:
                if not bool(settings.get("default_city")):
                    print("No default city set. Please provide a city name.")
                    continue
                city_name = list(settings.get("default_city").keys())[0]
                state_code = settings.get('default_city').get(city_name).get('state_code', None)
                country_code = settings.get('default_city').get(city_name).get('country_code', None)
            weather_data = get_weather_data(encoded_key, city_name, state_code, country_code, units)
            weather_data = weather_data.json()
            if 'cod' in weather_data and weather_data['cod'] == 200:
                print(weather_data['name'])
                print(weather_data['sys']['country'])
                print(weather_data['weather'])
                print(weather_data['main'])

                coord = (weather_data['coord'])
                latitude = coord['lat']
                longitude = coord['lon']
                city_time = city_timezone(latitude, longitude)
                print("Current time:", city_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            else:
                print("Error: city not found.")
        elif choice == '4':
            print("\nFavorite cities Menu:")
            list_favorite_cities = list(settings.get("favorite_cities").keys())
            if not list_favorite_cities:
                print("No favorite cities found.")
                continue
            for idx, city in enumerate(list_favorite_cities, 1):
                print(f"{idx}. {city}")
            choice_favorite_city = input("Enter the number of the favorite city to fetch weather: ")
            units = input("Enter temperature units (C/F): ").upper()
            for idx, city in enumerate(list_favorite_cities, 1):
                if str(idx) == choice_favorite_city:
                    city_name = list_favorite_cities[idx-1]
                    state_code = settings.get('favorite_cities').get(city_name).get('state_code', None)
                    country_code = settings.get('favorite_cities').get(city_name).get('country_code', None)
            weather_data = get_weather_data(encoded_key, city_name, state_code, country_code, units)
            weather_data = weather_data.json()
            if 'cod' in weather_data and weather_data['cod'] == 200:
              print(weather_data['name'])
              print(weather_data['sys']['country'])
              print(weather_data['weather'])
              print(weather_data['main'])

              coord = (weather_data['coord'])
              latitude = coord['lat']
              longitude = coord['lon']
              city_time = city_timezone(latitude, longitude)
              print("Current time:", city_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

