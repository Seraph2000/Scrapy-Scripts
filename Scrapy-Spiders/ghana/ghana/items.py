# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GhanaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_title = scrapy.Field()
    subcategory1 = scrapy.Field()
    subcategory2 = scrapy.Field()
    subcategory3 = scrapy.Field()
    subcategory4 = scrapy.Field()
    is_Subcategory4_last = scrapy.Field()
    #pass
