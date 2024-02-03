from datetime import datetime
from tkinter import *

import requests

# Initialize Window

root = Tk()
root.geometry("430x400")  # size of the window by default # to make the window size fixed
# title of our window
root.title("Cloudburst")

# ----------------------Functions to fetch and display weather info
city_value = StringVar()


def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


def showWeather():
    # Enter your API key, copied from the OpenWeatherMap dashboard
    api_key = "a08955ad82d15f896550dbf7ebe9007b"  # sample API

    # Get city name from the user from the input field (later in the code)
    city_name = city_value.get()

    if not city_name:
        tfield.delete("1.0", "end")
        tfield.insert(INSERT, "\n\tPlease enter a city name!")
        return

    # API url
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

    # Get the response from the fetched URL
    response = requests.get(weather_url)

    # changing response from JSON to python readable
    weather_info = response.json()

    tfield.delete("1.0", "end")  # to clear the text field for every new output

    # as per API documentation, if the cod is 200, it means that weather data was successfully fetched
    if response.status_code == 200:
        kelvin = 273  # value of kelvin

        # -----------Storing the fetched values of weather of a city

        temp = int(weather_info['main']['temp'] - kelvin)  # converting default Kelvin value to Celsius
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        # assigning Values to our weather variable, to display as output

        weather = f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°" \
                  f"\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at " \
                  f"{sunset_time}\nCloud: {cloudy}%\nInfo: {description} "
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter a valid City Name !!"

    tfield.insert(INSERT, weather)  # to insert or send value in our Text Field to display output


# ------------------------------Frontend part of code - Interface

Label(root, text='Enter City Name', font='Times 14').pack(pady=10)

Entry(root, textvariable=city_value, width=24, font='Verdana 14', justify='center').pack()

Button(root, command=showWeather, text="Check Weather", font="Times 10", bg='black', fg='white',
       activebackground="grey", padx=5, pady=5).pack(pady=20)

# to show output
Label(root, text="The Weather is:", font='Times 14').pack(pady=10)

tfield = Text(root, width=46, height=10, padx=10, pady=10)
tfield.pack()

root.mainloop()
