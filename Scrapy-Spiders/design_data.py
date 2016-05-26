# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from maxine.items import MaxineItem



class Maxine1Spider(CrawlSpider):
    name = "test3"
    allowed_domains = ["100percentdesign.co.uk"]

    def start_requests(self):
        init_url = 'http://www.100percentdesign.co.uk/page.cfm/action=ExhibList/ListID=10/t=m/'
        yield Request(init_url, callback=self.parse_pages)

    def parse_pages(self, response):
        page = response.xpath('//a[@class="listnavpagenum"]/@href').extract()
        test_duplicates = []
        i = 0
        for x in page:
            results = []
            if x not in test_duplicates:
                results.append(x)
                test_duplicates.append(x)
            for y in results:
                page_url = x
                #print page_url
                yield Request(page_url, callback=self.parse_initial_url)
                

    def parse_initial_url(self, response):
        #work out how to put images into image folder
        #item['image_urls'] = selector.xpath('//a[@class="exhib_status exhib_status_interiors"]/img/@src').extract()
        n = 0
        title = response.xpath('//div[@class="ez_merge5"]/a/text()').extract() #48
        item_url = response.xpath('//div[@class="ez_merge4"]/a/@href').extract() #48
        images = response.xpath('//div[@class="ez_merge4"]//img/@src').extract() #48
        #image_urls = response.xpath('//div[@class="ez_merge4"]//img/@src').re('^.*ExhibID.*$') #43
        for e in title:
            item = MaxineItem()
            item['title'] = title[n]
            item['item_url'] = item_url[n]
            item['images'] = images[n]
            item['count'] = n
            #item['count'] = n
            n += 1
            #yield item
            yield Request(item['item_url'], callback=self.parse_data1, meta=dict(item=item))

    def parse_data1(self, response):
        tot = 0
        #item = MaxineItem()
        #might want to experiment with response.meta, if anything goes wrong!
        item = response.meta['item']
        details = response.xpath('//div[@id="ez_entry_contactinfo"]//text()').extract()
        
        #Create address from available details
        seq = ''
        for j in details:
            if re.match(r'((?:C|c)ontact|www\.|http://|(?:S|s)tand|\r\n\t?|[0-9\+\-_ ]{8,}|\w+[0-9]{3})',j):
                a = j
            else:
                seq = seq + j + ", "
                if re.match(r'^.*\s*(UK|Uk|uk|(?:U|u)nited\s*(?:K|k)ingdom|(?:E|e)ngland|(?:i|I)taly|(?:S|s)wizerland)\s*,\s*\n*$', seq):
                    country = re.match(r'.*\s*(UK|Uk|uk|(?:U|u)nited\s*(?:K|k)ingdom|(?:E|e)ngland|(?:i|I)taly|(?:S|s)wizerland)\s*,\s*\n*$', seq).group(1)
                    seq = re.sub(r'(UK|Uk|uk|(?:U|u)nited\s*(?:K|k)ingdom|(?:E|e)ngland|(?:i|I)taly|(?:S|s)wizerland)\s*,\s*$','', seq)
                    seq = seq + country + "."

        address = seq

                                    

        item['address'] = address
        #item['telephone'] = response.xpath('//div[@id="ez_entry_contactinfo"]//text()').re('^\s*?[0-9\+_\-() ]{8,}\s*\n*$')
        item['website'] = response.xpath('//div[@id="ez_entry_contactinfo"]//text()').re('^.*?www..*?$')
        tel = response.xpath('//div[@id="ez_entry_contactinfo"]//text()').re('^\s*?[0-9\+_\-() ]{8,}\s*\n*$')
        for x in tel:
            if re.match(r'(\r\n\t?|\s{3,}|\n)', x):
                y = x
            else:
                item['telephone'] = x
        
        yield item



            

