import scrapy
from ..items import FfetchItem

class FfetcherSpider(scrapy.Spider):
    #Spider Name
    name = 'ffetcher'
    #Initializing to start scraping from page 1
    page_number = 1
    #page_url
    start_urls = ['https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page=1']

    def parse(self, response):
        items = FfetchItem()
        #getting urls for all the products
        product_url = response.css('._0a5d39 a').css('::attr(href)').getall()

        for product in product_url: #Looping through all the products
            link = response.urljoin(product)
            yield scrapy.Request(link, callback=self.parse_links)

        # Pagination
        next_page = "https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page=" + str(
        FfetcherSpider.page_number)

        # Looping through all the pages
        if FfetcherSpider.page_number < 80:
            FfetcherSpider.page_number += 1
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_links(self, response):
        items = FfetchItem()

        #Extracting data
        name = response.css('._3c73f1::text').get()  # Product Name
        brand = response.css('._e4b5ec::text').get()  # Product Brand
        price = response.css('._0f635f::text').get()  # Product Price
        image_url = response.css('#slice-pdp > div > div._53a765 > div._d47db0 > div._116295 > meta:nth-child(1)').css('::attr(content)').get()  # Image Url
        product_id = response.css('head > link  :nth-child(4)').css('::attr(href)').get()
        product_url = response.urljoin(product_id) #joining with base url to get complete url

        #Saving Data
        items['name'] = name
        items['brand'] = brand
        items['price'] = price
        items['image_url'] = image_url
        items['product_url'] = product_url

        yield items