import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] #What the spider is allowed to scrape so it does not go off tangent
    start_urls = ["https://books.toscrape.com"] #Where to start

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()   
            if relative_url is not None:
                if "catalogue" in relative_url:
                    book_url = "https://books.toscrape.com/" + relative_url
                    
                else:
                    book_url = "https://books.toscrape.com/catalogue/" + relative_url
            yield response.follow(book_url, callback = self.parse_book_page)

        next_page = response.css("li.next a ::attr(href)").get()
        if next_page is not None:
            if "catalogue" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
                
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):
        response.css(".product_main h1::text").get()
             
        