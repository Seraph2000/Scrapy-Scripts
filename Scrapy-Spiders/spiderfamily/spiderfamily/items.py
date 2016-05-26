# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderfamilyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    spider_link = scrapy.Field()
    common_name = scrapy.Field()
    spider_description = scrapy.Field()
    spider_origin = scrapy.Field()
    spider_images = scrapy.Field()
    order_family = scrapy.Field()
    genus_species = scrapy.Field()
    #pass
