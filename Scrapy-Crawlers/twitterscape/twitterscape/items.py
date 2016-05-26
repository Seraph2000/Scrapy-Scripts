# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterscapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userNumber = scrapy.Field()
    userName = scrapy.Field()
    userStatus = scrapy.Field()
    userID = scrapy.Field()
    #pass
