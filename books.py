import scrapy
from scrapy.crawler import CrawlerProcess
import json

class BookSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com']
    print(start_urls)

    def __init__(self):
        self.list_books = []

    def parse(self, response):
        for books in response.css('article.product_pod'):
            books_data = {
                'title': books.css('a::attr(title)').get(),
                'price:': books.css('p.price_color::text').get(),
            }
            self.list_books.append(books_data)
        

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        else:
            with open('books.json', 'w') as f:
                json.dump(self.list_books, f, indent=4)

process = CrawlerProcess()
process.crawl(BookSpider)
process.start()