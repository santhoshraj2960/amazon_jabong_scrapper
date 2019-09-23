import scrapy
import traceback
import re
from jabong_scrapper.items import JabongScrapperItem
import json

processed_start_url = False

unsuccess_list = []
class JabongSpider(scrapy.Spider):
    name = "jabong"
    start_urls = [
        "http://www.jabong.com/women/clothing/tops-tees-shirts/shirts/?source=topnav_women"
    ]
    

    def parse(self, response):
        total_items = json.loads(response.css('#facet-json::text').extract()[0])['productCnt']
        new_url = response.url + '&ax=1&page=1&limit={}&sortField=popularity&sortBy=desc'.format(total_items)
        print 'new_url = ', new_url
        print "************ Parse function called ***********************"
        yield scrapy.Request(new_url, callback=self.parse_fullpage)
        

    def parse_fullpage(self, response):
        total_items = response.css('.product-tile a::attr(href)').extract()
        for item in total_items:
            item_link = 'http://www.jabong.com{}'.format(item)
            yield scrapy.Request(item_link, callback=self.parse_question)

    def parse_question(self, response):
        brand = response.css('.brand::text').extract()[0]
        product_title = response.css('.product-title::text').extract()[0]
        try:
            original_price = response.css('#pdp-price-info .actual-price::text').extract()[0]
        except IndexError:
            original_price = response.css('.actual-price::text').extract()[0]
        all_sizes = ','.join(response.css('#size-block ul li a span::text').extract())
        other_available_colurs = ','.join(response.css('.color ul li a::attr(title)').extract())
        images = []
        for item in  response.css('.product-image img::attr(data-img-config)').extract():
            images.append(json.loads(item)['base_path']+'.jpg')
        category_hierarchy = ' > '.join(response.css('.product-image a::attr(href)').extract()[0].strip('/').split('/')[3:])
        label =  response.css('.prod-main-wrapper li label::text').extract()
        label_description = response.css('.prod-main-wrapper li span::text').extract()
        product_description = ''
        if len(label) == len(label_description):
            for count,item in enumerate(label):
                product_description += '{} : {}\n'.format(item.encode('utf-8'), label_description[count].encode('utf-8'))
        else:
            label_description = 'not acailable'
        product_id = response.css('#size-block ul li a::attr(data-simple-sku)').extract()[0].split('-')[0]
        callback = lambda response: self.testfunction(response, product_id, brand, product_title, original_price, 
            all_sizes, other_available_colurs, images, category_hierarchy, product_description)
        yield scrapy.Request('http://www.jabong.com/pdp/getCouponOffer?sku={}'.format(product_id), 
                   meta={'brand': brand, 'product_title': product_title, 'original_price': original_price, 'all_sizes': all_sizes,
                   'other_available_colurs': other_available_colurs, 'images': images, 'category_hierarchy':category_hierarchy,
                   'product_description':product_description, 'brand':brand},
                   callback=self.process_discount_price)

    def process_discount_price(self, response):
        item = JabongScrapperItem()
        title_product = response.meta['product_title']
        print 'product_title = ', title_product
        brand = response.meta['brand']
        print 'brand = ', brand
        original_price = response.meta['original_price']
        print 'original_price = ', original_price
        if len(json.loads(response.body)['couponOffer']) > 0:
            price_after_discount = json.loads(response.body)['couponOffer']['default']
            price_after_discount['voucher-info'] = json.loads(response.body)['couponInfo']['voucher_info']
        else:
            price_after_discount = 'No discount on this article'
        description = response.meta['product_description']
        print 'description = ', description
        category_hierarchy = response.meta['category_hierarchy']
        print 'category_hierarchy = ', category_hierarchy
        images = response.meta['images']
        print 'images = ', images
        all_sizes = response.meta['all_sizes']
        print 'all_sizes = ', all_sizes
        original_price = response.meta['original_price']
        print 'original_price = ', original_price
        other_available_colurs = response.meta['other_available_colurs']
        print 'other_available_colurs = ', other_available_colurs
        item['name'] = title_product
        item['brand'] = brand
        item['original_price'] = original_price
        item['price'] = price_after_discount
        item['description'] = description
        item['images'] = images
        item['category_hierarchy'] = category_hierarchy.replace('\n', ' ')
        item['sizes_available'] = all_sizes
        item['other_available_colurs'] = other_available_colurs
        yield item
    '''start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)'''