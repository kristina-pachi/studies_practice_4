# 2. Получение данных о погоде через API.

import requests  # type: ignore

api_url = "https://api.openweathermap.org/data/2.5/weather"


# выполнение HTTP‑запроса
def fetch_weather(lat: float, lon: float, api_key: str) -> dict | None:
    """
    Выполняет HTTP‑запрос к API OpenWeatherMap
    и возвращает сырые данные о погоде.

    :param lat: Широта в градусах.
    :type lat: float
    :param lon: Долгота в градусах.
    :type lon: float
    :param api_key: Ключ доступа к API OpenWeatherMap.
    :type api_key: str
    :returns: JSON‑ответ в виде словаря или None, если ошибка.
    :rtype: dict | None
    :raises Exception: При сетевых ошибках или таймауте.
    """

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
    """
    Извлекает и валидирует данные о погоде из JSON‑ответа API.

    :param data: Сырые данные, полученные от OpenWeatherMap.
    :type data: dict
    :returns: Словарь с обработанной информацией о погоде или None при ошибке.
    :rtype: dict | None
    :raises KeyError: Если в данных отсутствуют необходимые поля.
    :raises TypeError: Если значения имеют неверные типы.
    """

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
