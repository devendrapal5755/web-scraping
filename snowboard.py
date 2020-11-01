import scrapy #scrapy for extract data from website
from ..items import BtSnowboardItem #import class from items to run & save all details

# make below class for start the extract data from below url
class SnowboardSpider(scrapy.Spider):
    name = 'snowboard'
    page_number = 1
    start_urls = [
        'https://www.blue-tomato.com/en-AT/products/categories/Snowboard+Shop-00000000/gender/boys--girls--men--women/?page=1'

           ]

    def parse(self, response):
        items = BtSnowboardItem()

        #getting urls for all the products
        product_url = response.css('li').css('::attr(data-href)').getall()

        for product in product_url:  #Looping through all the products
            link = response.urljoin(product)
            yield scrapy.Request(link, callback=self.parse_links)

        # Pagination
        next_page = "https://www.blue-tomato.com/en-AT/products/categories/Snowboard+Shop-00000000/gender/boys--girls--men--women/?page=" + str(
        SnowboardSpider.page_number)

        # Looping through all the pages
        if SnowboardSpider.page_number < 35:
            SnowboardSpider.page_number += 1
            yield scrapy.Request(url=next_page, callback=self.parse)


#this parse use for extract data by given below name
    def parse_links(self, response):

        items = BtSnowboardItem()
        # Extracting data from each link
        name = response.css('#variantName::text').get()
        brand = response.css('.c-details-box__name span:nth-child(1)::text').get()
        price = response.css('.c-details-box__price-current::text').get()
        image_url = response.css('#imageViewer > img').css('::attr(src)').get()
        product_id = response.css('head > meta:nth-child(14)').css('::attr(content)').get()
        product_url = response.urljoin(product_id)


# save data in items
        items['name'] = name
        items['brand'] = brand
        items['price'] = price
        items['image_url'] = image_url
        items['product_url'] = product_url


        yield items

