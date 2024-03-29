import requests
from lxml import html
import csv
from pprint import pprint

# Определение целевого URL
url = "https://www.cbr.ru/currency_base/daily/"

# Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
try:
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})

    if response.status_code == 200:
        print("Успешный запрос API по URL: ", response.url)
    else:
        print("Запрос API отклонен с кодом состояния:", response.status_code)

except requests.exceptions.RequestException as e:
    print("Ошибка в осущественнии HTML запроса:", e)

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
tree = html.fromstring(response.text)

# Использование выражения XPath для выбора всех строк таблицы валют
currencies = tree.xpath("//tr")

# Создание пустого списка для последующего помещения в него мнформации обо всех валютах
currency_list = []

# Заполнение списка валют словарями с информацией о каждой валюте
for currency_item in currencies:

    # Использование выражения XPath для получения списка с текстовыми данными о каждой валюте
    curr_info_list = currency_item.xpath("./td/text()")
    if len(curr_info_list):
        currency = {}

        # Обработка данных для столбца 'код валюты' (переводим из str в int)
        try:
            currency['digital_code'] = int(curr_info_list[0])
        except ValueError:
            currency['digital_code'] = None

        # Обработка данных для стлбца 'буквенный код' не нужна
        currency['letter_code'] = curr_info_list[1]

        # Обработка данных для столбца 'единицы' (переводим из str в int)
        try:
            currency['units'] = int(curr_info_list[2])
        except ValueError:
            currency['units'] = None

        # Обработка данных для столбца 'название валюты' не нужна
        currency['currency_name'] = curr_info_list[3]

        # Обработка данных столбца 'курс' (переводим из str в float)
        try:
            currency['exchange_rate'] = float(curr_info_list[4].replace(',', '.'))
        except ValueError:
            currency['exchange_rate'] = None

        currency_list.append(currency)

# Сохранение полученной информации в csv файл
csv_file = 'exchange_rates.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    #     первая строка файла будет иметь названия полей
    fieldnames = ['digital_code', 'letter_code', 'units', 'currency_name', 'exchange_rate']
    writer = csv.DictWriter(f, fieldnames=fieldnames, quotechar='|')
    # Запись названий столбцов в первую строку
    writer.writeheader()
    # Запись данных о валютах
    writer.writerows(currency_list)
