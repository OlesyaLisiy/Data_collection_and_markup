import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
ua = UserAgent()
# print(ua.random)

# Запрос веб-страницы
url = 'https://www.boxofficemojo.com'
headers = {
    "UserAgent": ua.chrome # random
}
params = {
    "ref_": "bo_nb_hm_tab"
}

session = requests.session()

response = session.get(url+"/intl", params=params, headers=headers)

# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

rows = soup.find_all("tr")

films = []

for row in rows[2: -9]:
    film = {}
    # area_info = row.find('td', {'class': 'a-text-left mojo-header-column mojo-truncate mojo-field-type-area_id'}).find('a')
    area_info = row.find('td', {'class': 'a-text-left mojo-header-column mojo-truncate mojo-field-type-area_id'}).findChildren()[0]
    film['area'] = [area_info.getText(),
                    url + area_info.get('href')]

    weekend_info = row.find('td', {'class': 'a-text-left mojo-field-type-date_interval'}).findChildren()[0]
    film['weekend'] = [weekend_info.getText(),
                       url + weekend_info.get('href')]

    film['releases'] = int(row.find('td', {'class': 'a-text-right mojo-field-type-positive_integer'}).getText())

    first_release_info = row.find('td', {'class': 'a-text-left mojo-field-type-release mojo-cell-wide'}).findChildren()[0]
    film['first_release'] = [first_release_info.getText(),
                            url + first_release_info.get('href')]
    try:
        distributor_info = row.find('td', {'class': 'a-text-left mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(),
                              url + distributor_info.get('href')]
    except:
        print('Exception with first_release, object = ', film['first_release'])
        film['distributor'] = None

    film['gross'] = row.find('td', {'class': 'a-text-right mojo-field-type-money'}).getText()

    films.append(film)

pprint(films)
# Вывод HTML-содержимого веб-страницы
# print(soup.prettify())
