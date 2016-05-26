##Seraphina Anderson, 9/5/2016
##
## -*- coding: utf-8 -*-


import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from spiderfamily.items import SpiderfamilyItem



class Spiders(CrawlSpider):
    name = "spiders"

    def start_requests(self):
        url  = 'http://mamba.bio.uci.edu/~pjbryant/biodiv/spiders'
        yield Request(url, callback=self.parse_spiders)


    def parse_spiders(self, response):
        item = SpiderfamilyItem()
        get_url = response #this gets us current URL crawling!
        spider_url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        urls = response.xpath('//tr/td/a/@href').extract() #204
        for e in urls:
            url = "http://mamba.bio.uci.edu/~pjbryant/biodiv/spiders/" + str(e)
            #print url
            item['spider_link'] = url
            yield Request(url, callback=self.parse_categories, meta=dict(item=item))


    def parse_categories(self, response):
        item = response.meta['item']
        get_url = response #this gets us current URL crawling!
        spider_url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        #print "Testing: " + str(spider_url)
        
        if response.xpath('//p[@class="CommonName"]/text()'):
            common_name = response.xpath('//p[@class="CommonName"]/text()').extract()
            common_name = common_name[0].strip()
            item['common_name'] = common_name
        else:
            item['common_name'] = ''
        if response.xpath('//p/span[@class="Text"]/text()'):
            description = response.xpath('//p/span[@class="Text"]/text()').extract()
            desc = " ".join(e.strip() for e in description)
            desc = desc.replace(' Back to ', '')
            desc = desc.strip()
            item['spider_description'] = desc
        else:
            item['spider_description'] = ''
        if response.xpath('//td/img/@src').extract():
            item['spider_images'] = response.xpath('//td/img/@src').extract()
        else:
            item['spider_images'] = ''
        if response.xpath('//p[@class="OrderFamily"]/text()'):
            order_family = response.xpath('//p[@class="OrderFamily"]/text()').extract()
            order_family = order_family[0].strip()
            item['order_family'] = order_family
        else:
            item['order_family'] = ''
        if response.xpath('//span[@class="GenusSpecies"]/text()'):
            genus_species = response.xpath('//span[@class="GenusSpecies"]/text()').extract()
            genus_species = genus_species[0].strip()
            item['genus_species'] = genus_species
        else:
            item['genus_species'] = ''
            
        yield item


#transfer to CSV:
#scrapy crawl spiders -o spiders1.csv
        
