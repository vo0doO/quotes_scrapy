import scrapy
import hashlib


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    count = 0

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = f"{url}/tag/{tag}"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            QuotesSpider.count += 1
            text = quote.css("span.text::text").get()
            yield {
                "hash": hashlib.md5(text.encode('utf-8')).hexdigest(),
                'text': text,
                'author': quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        yield from response.follow_all(css="ul.pager a", callback=self.parse)

        self.log(f"count: {QuotesSpider.count}")
