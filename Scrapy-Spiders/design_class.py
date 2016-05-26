# -*- coding: utf-8 -*-
import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from maxine.items import MetaItem



class DesignclassSpider(CrawlSpider):
    name = "class1"
    def start_requests(self):
        class_url = 'http://oami.europa.eu/designclass/locarnoClassification/find?linkMenu=true'
        yield Request(class_url, callback=self.parse_init_page)


    #scrape classes and subclasses
    def parse_init_page(self, response):
        item = MetaItem()
        #1 class_number = scrapy.Field()
        class_no = response.xpath('//h2//span[1]/text()').re('\d+')
        #2 class_name = scrapy.Field()
        class_name = response.xpath('//h2//span[2]/text()').extract()
        i = 0
        while i < len(class_name):
            nums = response.xpath('//dl')[i].re('0\d+')
            subnames = response.xpath('//dl')[i].re('<dd\s*class="(?:first)?\s*locarnodd">(.*?)?</dd>')
            item['class_no'] = class_no[i]
            item['class_name'] = class_name[i]
            item['subclass_nos'] = nums
            item['subclass_names'] = subnames
            item['counter'] = i + 1
            i += 1
            yield item



#make a csv file: scrapy crawl class1 -o classes.csv
#make a json file: scrapy crawl class1 -o classes.json
            
