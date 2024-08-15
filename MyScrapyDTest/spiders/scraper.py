# import the required modules
from scrapy.spiders import Spider
 
class MySpider(Spider):
    # specify the spider name
    name = 'product_scraper'
    start_urls = ['https://www.scrapingcourse.com/ecommerce/']
 
    # parse HTML page as response
    def parse(self, response):
        # extract text content from the ul element
        products = response.css('ul.products li.product')
        
        data = []
 
        for product in products:
            # parent = product.css('li.product')
            product_name = product.css('h2.woocommerce-loop-product__title::text').get()
            price = product.css('bdi::text').get()
 
            # append the scraped data into the empty data array
            data.append(
                {
                'product_name': product_name,
                'price': price,
            }
            )
 
        # log extracted text
        self.log(data)
