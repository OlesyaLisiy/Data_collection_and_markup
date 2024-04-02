import scrapy
from scrapy.http import HtmlResponse
from HW.HW_5.bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/genres/3036/"]

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//div[@class = 'pagination-next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@data-title='Все в жанре «Литература на французском языке для детей»']//a[@class = 'product-title-link']/@href").getall()
        url = 'https://www.labirint.ru'
        for link in links:
           yield response.follow(url + link, callback=self.book_parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        author = response.xpath("//a[@data-event-label='author']/text()").getall()
        publisher = response.xpath("//a[@data-event-label='publisher']/text()").getall()
        year = response.xpath("//div[@class='publisher']/text()").getall()
        series = response.xpath("//a[@data-event-label='series']/text()").getall()
        price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        link = response.url
        yield BookparserItem(name=name, author=author, publisher=publisher, year=year, series=series,
                             price=price, rating=rating, link=link)
