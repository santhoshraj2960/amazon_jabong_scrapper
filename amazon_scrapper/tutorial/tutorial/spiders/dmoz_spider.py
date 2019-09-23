
import scrapy
import traceback
import re
import time
from tutorial.items import DmozItem

unsuccess_list = []
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    rotate_user_agent = True
    start_urls = [
        "http://www.amazon.com/s/ref=fs_w_clo_drs_spr2_w2w?rh=i%3Afashion-brands%2Cn%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cn%3A2346728011%2Cp_6%3AATVPDKIKX0DER&bbn=10445813011&sort=date-desc-rank&ie=UTF8"
    ]

    def parse(self, response):
        print "************ Parse function called ***********************"
        i = 0
        while i < len(response.css('.s-result-item')):
            title_product = response.css('.s-result-item')[i].css('.s-access-detail-page').css('a::attr(title)').extract()[0]
            print 'title_product = ', title_product
            item_link= response.css('.s-result-item')[i].css('.s-access-detail-page').css('a::attr(href)').extract()[0]
            print 'item_link = ', item_link
            yield scrapy.Request(item_link, callback=self.parse_question)
            i += 1

        if response.css('#pagnNextLink::attr(href)').extract()[0]:
            url = 'http://www.amazon.com{}'.format(response.css('#pagnNextLink::attr(href)').extract()[0])
            # trying to sleep after scrapping all the items after every 5 pages (but doen't help for ip getting banned)
            '''page_number = int(url.split('page=')[1].split('&')[0])
            print 'page_number = ', page_number
            if int(page_number)%5 == 0:
                time.sleep(300)'''
            print '***************inside if url = **************', url
            yield scrapy.Request(url, callback=self.parse)

            
    #This function is the one which parses every item of a page and gets the details about it
    def parse_question(self, response):
        item = DmozItem()
        title_product = response.css('#productTitle::text').extract()[0]
        print 'product_title = ', title_product
        if response.css('#brand::text').extract():
            brand = response.css('#brand::text').extract()[0].strip()
        else:
            brand = response.css('#brand::attr(href)').extract()[0].split('/')[1]
        print 'brand = ', brand
        original_price = response.css('#price .a-span12::text').extract()[0]
        print 'original_price = ', original_price
        try:
            price_after_discount = response.css('#price #priceblock_ourprice::text').extract()[0]
            print 'price_after_discount = ', price_after_discount
        except IndexError:
            print 'no discount for this article.'
        description = ','.join(response.css('#feature-bullets .a-list-item::text').extract())
        print 'description = ', description
        category_hierarchy = re.sub(' +',' ','>'.join(response.css('#wayfinding-breadcrumbs_feature_div .a-list-item .a-color-tertiary::text').extract()))
        print 'category_hierarchy = ', category_hierarchy
        images = response.css('#altImages li img::attr(src)').extract()
        print 'images = ', images
        all_sizes = response.css('#native_dropdown_selected_size_name option::attr(data-a-html-content)').extract()
        print 'all_sizes = ', all_sizes
        if not all_sizes:
            all_sizes = response.css('#variation_size_name .selection::text').extract()[0]
        else:
            all_sizes = ','.join(all_sizes)
        if not original_price.strip():
            original_price = price_after_discount
        else:
            original_price = original_price
        item['name'] = title_product
        item['brand'] = brand
        item['original_price'] = original_price
        item['price'] = price_after_discount
        item['description'] = description
        item['images'] = images
        item['category_hierarchy'] = category_hierarchy.replace('\n', ' ')
        item['sizes_available'] = all_sizes
        yield item
    '''start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)'''