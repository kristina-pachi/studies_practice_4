# 1. Парсинг новостей с веб-сайта.


import re
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://lenta.ru"

# проверка доступности сайта
def check_site(url: str) -> bool:
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 500
    except Exception:
        return False

# загрузка HTML-кода страницы
def load_html(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception:
        return None

# поиск карточек новостей
def parse_cards(html: str):
    soup = BeautifulSoup(html, "lxml")
    # ищем элементы, у которых класс начинается с card- и содержит только буквы
    cards = soup.find_all(class_=re.compile(r"^card-[a-z]+$"))
    return cards

# парсинг одной карточки
def parse_one_card(card):
    title_tag = card.find("h3")
    if not title_tag:
        return None

    title = title_tag.get_text(strip=True)
    link = card.get("href")

    if not link:
        return None

    full_link = urljoin(base_url, link)

    return {
        "title": title,
        "link": full_link
    }

# парсинг всех карточек
def parse_all_cards(cards):
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
    with open(filename, "w", encoding="utf-8") as f:
        for new in news:
            f.write(f"{new['№']}. {new['title']}: {new['link']}\n")


# cохранение в csv
def save_news_csv(news, filename="all_news_from_lenta_ru.csv"):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["№", "title", "link"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(news)


def run_parser():
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