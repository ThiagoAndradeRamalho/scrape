import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']

    def __init__(self):
        self.quotes_list = []

    def parse(self, response):
        quotes_list = []
        for quote in response.css('div.quote'):
            quote_data = {
               'text': quote.css('span.text::text').get(),
               'author': quote.css('small.author::text').get(),
            }
            self.quotes_list.append(quote_data)



        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            with open('quotes.json', 'w') as f:
                json.dump(self.quotes_list, f, indent=4)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()