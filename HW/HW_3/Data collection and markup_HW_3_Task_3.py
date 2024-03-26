# Поэкспериментируйте с различными методами запросов

from pymongo import MongoClient
from tokens import Atlas_User, Atlas_Pass, Atlas_Host
import json

uri = f"mongodb+srv://{Atlas_User}:{Atlas_Pass}@cluster0.{Atlas_Host}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Создание нового клиента и подключение к серверу
client = MongoClient(uri)

# Отправка пинга, чтобы подтвердить успешное подключение
try:
     client.admin.command('ping')
     print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
     print(e)

# Выбор базы данных и коллекции
db = client['library']
collection = db['books']

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# Изучение одного документа с помощью функции find_one()
document = collection.find_one()
print(f'Поля документа: {document.keys()}')

# Самая дешевая книга
min_price_book = collection.aggregate([
    {"$group": {"_id": "$title", "min_price": {"$min": "$price"}}},
    {"$sort": {"min_price": 1}}
])
min_price_book = list(min_price_book)[0]
print(f'Самая дешевая книга {min_price_book["_id"]} стоит £{min_price_book["min_price"]:.2f}')


# Самая дорогая книга
max_price_book = collection.aggregate([
    {"$group": {"_id": "$title", "max_price": {"$max": "$price"}}},
    {"$sort": {"max_price": -1}}
])
max_price_book = list(max_price_book)[0]
print(f'Самая дорогая книга {max_price_book["_id"]} стоит £{max_price_book["max_price"]:.2f}')

