import scrapy
import hashlib


class AuthorsSpider(scrapy.Spider):
    name = "authors"

    start_urls = ['https://quotes.toscrape.com/']

    def parse_authors(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        name = extract_with_css('.author-title::text')
        yield {
            'hash': hashlib.md5(name.encode('utf-8')).hexdigest(),
            'name': name,
            'birthdate': extract_with_css("span.author-born-date::text"),
            'bio': extract_with_css(".author-description::text")
        }

    def parse(self, response):
        author_links = response.css(".author + a")
        yield from response.follow_all(author_links, self.parse_authors)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)
