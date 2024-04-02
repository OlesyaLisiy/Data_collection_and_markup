from pymongo import MongoClient
from HW.HW_5.tokens import Atlas_User, Atlas_Pass, Atlas_Host
import json

uri = f"mongodb+srv://{Atlas_User}:{Atlas_Pass}@cluster0.{Atlas_Host}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['labirint_books']
collection = db['labirintru']
documents = list(collection.find())

with open('labirint_books.json', 'w', encoding='utf-8') as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)
    print(f"Документы сохранены в файл labirint_books.json")