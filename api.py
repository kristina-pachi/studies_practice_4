# 2. Получение данных о погоде через API.

import requests

api_url = "https://api.openweathermap.org/data/2.5/weather"


# выполнение HTTP‑запроса
def fetch_weather(lat: float, lon: float, api_key: str) -> dict | None:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(api_url, params=params, timeout=5)

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:
        return None

# извлечение данных из JSON
def parse_weather(data: dict) -> dict | None:
    try:
        city = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        # проверки типов
        if not isinstance(city, str):
            return None

        if not isinstance(temp, (float, int)):
            return None

        if not isinstance(description, str):
            return None

        if not isinstance(wind_speed, (float, int)):
            return None

        if not isinstance(humidity, int):
            return None

        # проверка влажности от 0 до 100 %
        if humidity < 0 or humidity > 100:
            return None

        return {
            "Город": city,
            "Температура": float(temp),
            "Описание погоды": description,
            "Скорость ветра": float(wind_speed),
            "Влажность": humidity
        }

    except Exception:
        return None


def get_weather(lat: float, lon: float, api_key: str) -> dict | None:
    raw = fetch_weather(lat, lon, api_key)
    if raw is None:
        return None

    return parse_weather(raw)


# вывод в консоль
print(get_weather(55.75396, 37.62039, "016409432b4afafeb6d7bf65196c12e2"))
