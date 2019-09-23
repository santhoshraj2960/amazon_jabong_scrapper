# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    original_price = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    category_hierarchy = scrapy.Field()
    sizes_available = scrapy.Field()
