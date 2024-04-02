# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    series = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()

