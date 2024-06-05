import streamlit as st

st.title('Weather App')


# Main function to orchestrate the process
def main():
    city_name = input('Enter the city name: ').lower()
    city_list = load_city_list('city.list.json')
    duplicate_cities = find_duplicate_cities(city_list)

    API_key = 'ec45812d74648049b38512b286f1ae6d'
    weather_data = get_city_weather(city_name, duplicate_cities, API_key)

    print(weather_data['main'])
    print(weather_data['weather'])

    coord = weather_data['coord']
    latitude = coord['lat']
    longitude = coord['lon']

    city_tz, city_time = get_city_time(latitude, longitude)
    print("City timezone:", city_tz)
    print("Local city time:", city_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))


# Run the main function
if __name__ == "__main__":
    main()
