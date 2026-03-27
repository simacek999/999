import requests
import time
import json
import os

CONFIG_FILE = "CONFIGURATION.txt"
API_URL = "https://api.openweathermap.org/data/2.5/weather"


def load_config():
    """Načte celý config ze souboru (JSON)."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("Soubor CONFIGURATION.txt nebyl nalezen.")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_weather(api_key, city):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "cz"
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 401:
        raise PermissionError("Neplatný API klíč.")
    if response.status_code == 404:
        raise ValueError("Město nebylo nalezeno.")
    if response.status_code != 200:
        raise RuntimeError(f"Chyba API: {response.status_code}")

    return response.json()


def print_weather(data):
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    clouds = data["clouds"]["all"]
    desc = data["weather"][0]["description"]

    print("\n==============================")
    print(f"🌍 Lokalita: {city}")
    print(f"🌡️ Teplota: {temp} °C")
    print(f"💧 Vlhkost: {humidity} %")
    print(f"☁️ Oblačnost: {clouds} %")
    print(f"📌 Popis: {desc}")
    print("==============================\n")


def main():
    print("Načítám config…")
    config = load_config()

    # tady bereš z JSONu
    api_key = config["api_key"]

    city = input("Zadej město: ")

    while True:
        try:
            weather_data = get_weather(api_key, city)
            print_weather(weather_data)
        except Exception as e:
            print(f"❌ Chyba: {e}")

        print("Čekám 10 sekund…")
        time.sleep(10)


if __name__ == "__main__":
    main()