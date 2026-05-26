# 1. Парсинг новостей с веб-сайта.


import re
import requests  # type: ignore
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://lenta.ru"


# проверка доступности сайта
def check_site(url: str) -> bool:
    """
    Проверяет доступность веб‑сайта с помощью HTTP‑запроса HEAD.

    :param url: URL сайта, доступность которого необходимо проверить.
    :type url: str

    :returns: True, если сайт отвечает кодом < 500, иначе False.
    :rtype: bool

    :raises Exception: При сетевых ошибках.
    """

    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 500
    except Exception:
        return False


# загрузка HTML-кода страницы
def load_html(url: str) -> str | None:
    """
    Загружает HTML‑код страницы по указанному URL.

    :param url: Адрес страницы, с которой требуется получить HTML.
    :type url: str

    :returns: HTML‑код страницы в виде строки или None при ошибке.
    :rtype: str | None

    :raises Exception: При ошибках сети или таймауте .
    """

    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception:
        return None


# поиск карточек новостей
def parse_cards(html: str):
    """
    Ищет карточки новостей в HTML‑коде страницы.

    :param html: HTML‑код страницы, полученный ранее.
    :type html: str

    :returns: Список найденных HTML‑элементов, карточек новостей.
    :rtype: list
    """

    soup = BeautifulSoup(html, "lxml")
    # ищем элементы, у которых класс начинается с card- и содержит только буквы
    cards = soup.find_all(class_=re.compile(r"^card-[a-z]+$"))
    return cards


# парсинг одной карточки
def parse_one_card(card):
    """
    Извлекает данные из одной карточки новости.

    :param card: HTML‑элемент карточки, найденный на странице.
    :type card: bs4.element.Tag

    :returns: Словарь с title и link на новость, None если данные некорректны.
    :rtype: dict | None

    :raises AttributeError: Если структура карточки не соответствует ожидаемой.
    """

    title_tag = card.find("h3")
    if not title_tag:
        return None

    title = title_tag.get_text(strip=True)
    link = card.get("href")

    if not link:
        return None

    full_link = urljoin(base_url, link)

    return {"title": title, "link": full_link}


# парсинг всех карточек
def parse_all_cards(cards):
    """
    Обрабатывает список карточек новостей и формирует итоговый список новостей.

    :param cards: Список HTML‑элементов карточек.
    :type cards: list

    :returns: Список словарей с данными о новостях, включая порядковый номер.
    :rtype: list
    """

    news = []
    n = 1

    for card in cards:
        item = parse_one_card(card)
        if item:
            item["№"] = n
            news.append(item)
            n += 1

    return news


# cохранение в txt
def save_news_txt(news, filename="all_news_from_lenta_ru.txt"):
    """
    Сохраняет список новостей в текстовый файл.

    :param news: Список словарей с новостями.
    :type news: list
    :param filename: Имя файла.
    :type filename: str, optional

    :returns: None.
    :rtype: None
    """

    with open(filename, "w", encoding="utf-8") as f:
        for new in news:
            f.write(f"{new['№']}. {new['title']}: {new['link']}\n")


# cохранение в csv
def save_news_csv(news, filename="all_news_from_lenta_ru.csv"):
    """
    Сохраняет список новостей в CSV‑файл.

    :param news: Список словарей с новостями.
    :type news: list
    :param filename: Имя CSV‑файла для сохранения.
    :type filename: str, optional

    :returns: None.
    :rtype: None
    """

    with open(filename, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["№", "title", "link"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(news)


def run_parser():
    """
    Запускает полный процесс парсинга новостей:
    проверяет сайт, загружает HTML,
    извлекает карточки и формирует итоговый список новостей.

    :returns: Список новостей или пустой список при ошибке.
    :rtype: list
    """

    if not check_site(base_url):
        print("Сайт недоступен, попробуйте позже.")
        return []

    html = load_html(base_url)
    if not html:
        print("Ошибка загрузки HTML")
        return []

    cards = parse_cards(html)
    news = parse_all_cards(cards)

    return news


# ввывод в консоль
print(*[f"{n['№']}. {n['title']}" for n in run_parser()], sep="\n")
