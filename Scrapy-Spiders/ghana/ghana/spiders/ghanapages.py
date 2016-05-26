#Seraphina Anderson, 9/5/2016

# -*- coding: utf-8 -*-

##
##import scrapy
##import re
##import json
##import csv
##from scrapy import Spider
##from scrapy.spiders import CrawlSpider, Rule
##from scrapy.linkextractors import LinkExtractor
##from scrapy.selector import Selector
##from scrapy.http import Request
##from ghana.items import GhanaItem


##
##class Ghana(CrawlSpider):
##    name = "ganalist"
##
##    def start_requests(self):
##
##        url  = 'http://yellowpages.com.gh/Home.aspx'
##        yield Request(url, callback=self.parse_weburl)
##

##    def parse_weburl(self, response):
##        item = GhanaItem()
##        get_url = response #this gets us current URL crawling!
##        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
##        cats = response.xpath('//div[@class="oneDirCat"]/h3/a/@href').extract()
##        cats = ['http://yellowpages.com.gh' + str(e) for e in cats]
##
##        for e in cats:
##            url = e
##            yield Request(url, callback=self.parse_categories, meta=dict(item=item))
##
##        
##
##    def parse_categories(self, response):
##        item = response.meta['item']
##        #test for subcategories => scrape more categories OR scrape directory info
##        
##
##        subcats = response.xpath('//div[@class="ActiveCat"]//a/@href').extract()
##        subcats = ['http://yellowpages.com.gh' + str(e) for e in subcats]
##        
##
##        yield Request(url, callback=self.parse_categories, meta=dict(item=item))
##
##
##        
##
##
####        category_title = scrapy.Field()
####        subcategory1 = scrapy.Field()
####        subcategory2 = scrapy.Field()
##        subcategory3 = scrapy.Field()
##        subcategory4 = scrapy.Field()
##        is_Subcategory4_last = scrapy.Field()




    

        
