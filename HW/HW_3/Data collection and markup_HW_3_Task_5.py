# Загрузите данные в ClickHouse и создайте таблицу для их хранения

# Регистрировалась в ClickHouse (https://clickhouse.com/) с помощью VPN

from clickhouse_driver import Client
from tokens import ClickHouse_User, ClickHouse_Pass, ClickHouse_Host
import json

# Подключение к серверу ClickHouse
client = Client(host=ClickHouse_Host,
                user=ClickHouse_User,
                secure=True,
                port=9440,
                password=ClickHouse_Pass)

# Создание базы данных (если она не существует)
client.execute("DROP DATABASE IF EXISTS library")
client.execute("CREATE DATABASE IF NOT EXISTS library")
client.execute("DROP TABLE IF EXISTS library.books")
client.execute('''
CREATE TABLE IF NOT EXISTS library.books (
    id UInt64,
    title String,
    price Float64,
    stock String
) 
ENGINE = MergeTree()
ORDER BY title
''')
print("Таблица books в базе library создана успешно.")

with open('all_books.json', 'r') as f:
    books = json.load(f)

print(f"Загружено {len(books)} документов.")

count = 0
for book in books:
    client.execute("""
        INSERT INTO library.books (
            id, title, price, stock
        ) VALUES""",
                   [(count,
                     book['title'] or "",
                     book['price'] or "",
                     book['stock'] or "")])
    count += 1

print(f"{count} строк загружено в таблицу {books}")

rows_num = client.execute("SELECT count() FROM library.books")
print(f"Количество строк в таблице books базы library: {rows_num[0][0]}")
