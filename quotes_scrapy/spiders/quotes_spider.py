import scrapy


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
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        yield from response.follow_all(css="li.next a", callback=self.parse)

        self.log(f"count: {QuotesSpider.count}")
