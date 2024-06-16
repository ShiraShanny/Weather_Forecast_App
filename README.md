# Weather_Forecast_App
The Weather Checker App is a simple web application built with Streamlit that allows users to check the current weather and local time for any city around the world. The app uses the OpenWeatherMap API to fetch weather data and the TimezoneFinder library to determine the local time.

Demo available at [Weather Checker App](https://shirashanny-weather-forecast-app-app-rjr2xe.streamlit.app/)
## Features
 Fetches current weather information for a specified city.
- Displays temperature, humidity, wind speed, and weather description.
- Shows the local time of the specified city based on its coordinates.
- Allows users to set a default city and add favorite cities for quick access.
## Installation
To set up the project, follow these steps:

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/)

### steps
1. **Clone the repository:**

   ```sh
   git clone https://github.com/ShiraShanny/Weather_Forecast_App.git
   cd Weather_Forecast_App
   ```
   

2. **Poetry install:**
If you haven't installed Poetry yet, you can do so by running:
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
or by following the instruction on [Poetry Python Website](https://python-poetry.org/docs/)

3. **Install dependencies:**
Run the following command to install all dependencies:

```sh
poetry install
```

4. **Activate the virtual environment created by Poetry:**

```sh
poetry shell
```

## Usage
To run the Weather Checker App, use the following command:

```sh
streamlit run app.py
```
Follow the prompts in the Streamlit interface to enter the city name and check the weather.

you can also find the script in the CoLab notebook [here](https://github.com/ShiraShanny/Weather_Forecast_App/blob/cc165009c357b4cc8fd3a00b0d517db6f0459d0e/Shira_Shanny_BIU_DS217_Python_Project_1_Weather_Forecast.ipynb)
## License
This project is licensed under the MIT License.

## Acnowledgements
 - streamlit
 - Google Colab
 - OpenWeatherMap API
 - TimezoneFinder

