import streamlit as st
import requests
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Weather Forecast App", page_icon="🌤️", layout="centered")

# ---- APP TITLE ----
st.title("🌦️ Real-Time Weather Forecast App")
st.write("Get instant weather updates for any city in the world!")

# ---- INPUT ----
city = st.text_input("Enter city name", placeholder="e.g. Mumbai, Maharashtra or Delhi, India")

# ---- API KEY ----
api_key = "YOUR_API_KEY_HERE"  # 🔹 Replace with your OpenWeather API key

# ---- WHEN USER CLICKS BUTTON ----
if st.button("Get Weather"):
    if city.strip():
        try:
            # 🧩 Handle extra spaces, commas
            city_clean = city.replace(",", "").strip()

            # ---- API URL ----
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_clean}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            # ---- SUCCESS ----
            if data["cod"] == 200:
                weather = data["weather"][0]["main"]
                description = data["weather"][0]["description"].title()
                icon = data["weather"][0]["icon"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]
                country = data["sys"]["country"]
                sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
                sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")

                st.markdown(f"### 📍 {city_clean.title()}, {country}")
                st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100)
                st.markdown(f"**🌤️ {weather} ({description})**")
                st.metric("🌡️ Temperature", f"{temp}°C", f"Feels like {feels_like}°C")
                st.metric("💧 Humidity", f"{humidity}%")
                st.metric("🌬️ Wind Speed", f"{wind} m/s")
                st.metric("🔼 Pressure", f"{pressure} hPa")
                st.markdown(f"🌅 **Sunrise:** {sunrise} UTC")
                st.markdown(f"🌇 **Sunset:** {sunset} UTC")

            else:
                st.error("❌ City not found! Please check the name and try again.")

        except Exception as e:
            st.error("⚠️ Something went wrong! Check your internet connection or API key.")
    else:
        st.warning("Please enter a city name to continue.")
