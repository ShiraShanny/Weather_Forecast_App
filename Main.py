import json
import datetime as dt
import pytz
from timezonefinder import TimezoneFinder

with open('city.list.json', encoding="utf8") as file:
    city_list = json.load(file)

from collections import Counter

city_names = [entry['name'].lower() for entry in city_list]
city_count = Counter(city_names)
duplicate_cities = [name for name, count in city_count.items() if count > 1]

import requests

city_name = input('Enter the city name: ')
API_key = 'ec45812d74648049b38512b286f1ae6d'

if city_name in duplicate_cities:
  state_code = input('Enter State code or NA: ')
  if state_code != 'NA':
    country_code = input('Enter Country code: ')
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{state_code},{country_code}&appid={API_key}&units=metric"""
    response = requests.get(url)
  else:
    country_code = input('Enter Country name: ')
    url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}&units=metric"""
else:
  url = f"""https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"""
  response = requests.get(url)

data = response.json()
print(data['main'])
print(data['weather'])

coord = (data['coord'])
latitude = coord['lat']
longitude = coord['lon']

tf = TimezoneFinder()
city_timezone = tf.timezone_at(lng=longitude, lat=latitude)
city_tz = pytz.timezone(city_timezone)
utc_now = dt.datetime.now(pytz.utc)
city_time = utc_now.astimezone(city_tz)
print("Current time:", city_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))