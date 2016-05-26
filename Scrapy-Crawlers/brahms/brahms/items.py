# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrahmsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    opus_name = scrapy.Field()
    opus_number = scrapy.Field()
    upvotes = scrapy.Field()
    views = scrapy.Field()
    subscribed = scrapy.Field()
    performer = scrapy.Field()
    year_composed = scrapy.Field()
    year_performed = scrapy.Field()
    #pass


#Rank by popularity
#or... categorize by: performer, year
