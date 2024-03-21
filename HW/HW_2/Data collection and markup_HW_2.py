import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import json
ua = UserAgent()

# Запрос веб-страницы
url = 'http://books.toscrape.com'
headers = {"UserAgent": ua.random}
session = requests.session()
all_books = []
count = 1

while True:
    page = f'page-{count}.html'
    response = session.get(url + '/catalogue/' + page, headers=headers)
    url_for_book = url + '/catalogue/'
    # Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', {'class': 'product_pod'})

    if not books:
        break

    for book in books:
        book_info = {}

        title_info = book.find('h3').find('a')
        book_info['title'] = title_info.getText()
        book_info['url'] = url_for_book + title_info.get('href')
        price_info = book.find('div', {'class': 'product_price'}).find('p', {'class': 'price_color'})
        book_info['price'] = float(price_info.getText()[1:])
        stock_info = book.find('div', {'class': 'product_price'}).find('p', {'class': 'instock availability'})
        book_info['stock'] = stock_info.getText().strip()
        all_books.append(book_info)
    print(f"Обработана {count} страница")
    count += 1

# сохранение данных в JSON-файл
file_name = 'all_books.json'
with open(file_name, 'w') as file:
    json.dump(all_books, file)