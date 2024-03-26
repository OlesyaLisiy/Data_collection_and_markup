# Загрузите данные, которые вы получили на предыдущем уроке
# путем скрейпинга сайта с помощью Buautiful Soup в MongoDB
# и создайте базу данных и коллекции для их хранения.

# Регистрировалась в Atlas (https://www.mongodb.com/cloud/atlas/register) с помощью VPN

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

# Чтение файла json и его загрузка в словарь data
with open('all_books.json') as f:
    data = json.load(f)

collection.insert_many(data)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')