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
from ftse.items import FtseItem



class ftseSpider(CrawlSpider):
    name = "ftse"

    def start_requests(self):
        url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX'
        yield Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        #generate pages here
        max_page = response.xpath('//div[@class="paging"]/p').re('.*?Page\s*1\s*of\s*(\d+).*')
        max_page = max_page[0]
        for x in range(1,int(max_page)+ 1):
            page = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX&page=' + str(x)
            yield Request(page, callback=self.parse_page)

    def parse_page(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        company_url = response.xpath('//td[@class="name"]/a/@href').extract()
        for i, e in enumerate(company_url):
            company_url = 'http://www.londonstockexchange.com' + company_url[i]
            yield Request(company_url, callback=self.parse_company_info)

        

    def parse_company_info(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        item = FtseItem()
        #item = response.meta['item']
        company_name = response.xpath('//li[@class="active"]/b/text()').extract()
        get_website = response.xpath('//a').re('.*?openerextlink.*')
        try:
            company_website = re.match('.*?title="(.*?)?">.*', get_website[0]).group(1)
        except:
            company_website = "error!"
        find = response.xpath('//tbody//text()').extract()
        get_index = int([find.index(e) for e in find if re.match('.*Company\s*address.*', e)])
        address_index = int(int(get_index[0]) + 2)
        get_address = str(find[address_index])

        
        item['company_name'] = company_name[0].strip()
        item['company_website'] = company_website
        item['company_address'] = get_address
        #print "Test #1: ", url
        yield item
        #yield Request(url, callback=self.parse_categories, meta=dict(item=item))


    

        
