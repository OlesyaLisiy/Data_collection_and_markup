# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from HW.HW_5.tokens import Atlas_User, Atlas_Pass, Atlas_Host

class BookparserPipeline:
    def __init__(self):
        uri = f"mongodb+srv://{Atlas_User}:{Atlas_Pass}@cluster0.{Atlas_Host}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri)
        self.mongobase = client['labirint_books']

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.count_page = 0

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        try:
            *_, id, _ = item['link'].split('/')
            item['_id'] = id
        except ValueError:
            item['_id'] = None

        _, name = item.get('name').split(':')
        item['name'] = name.strip()

        item['author'] = ', '.join(item['author'])

        item['publisher'] = ', '.join(item['publisher'])

        try:
            *_, year, _ = item['year'][1].split(' ')
            item['year'] = int(year)
        except ValueError:
            item['year'] = None

        item['series'] = ', '.join(item['series'])

        try:
            item['price'] = float(item['price'])
        except ValueError:
            item['price'] = None

        try:
            item['rating'] = float(item['rating'])
        except ValueError:
            item['rating'] = None

        collection.insert_one(item)

        self.count_page += 1
        print(f'Обработано {self.count_page} книг')

        return item