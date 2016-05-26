# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from ftse.items import FtseItem

class FtseSpider(CrawlSpider):
    name = "ftse1"
    #allowed_domains = ["londonstockexchange.com",".*"]
    handle_httpstatus_list = [404]

    #experiment with different start URLs
    def start_requests(self):
        init_url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX'
        #itit_url2 = '.*'
        yield Request(init_url, callback=self.parse_init_page)



    def parse_init_page(self, response):
        company_name = response.xpath('//a[@title="View detailed prices page"]/text()').extract()
        company_code = response.xpath('//td[@scope="row"]/text()').extract()
        #xpath - expression for more than one class?
        pages = response.xpath('//div[@class="paging"]').re('<a\s*href=.*?page=\d+"') #produces list of page URLs
        #test for duplicates
        i = 1
        #j = 0
        for x in pages:
            x = re.match('^.*?"(.*)?"$',x).group(1)
            url = 'http://www.londonstockexchange.com' + x
            url = url.replace('&amp;','&')
            results = ['http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX&page=1']
            test_duplicates = []
            if url not in test_duplicates:
                results.append(url)
                test_duplicates.append(url)
            #elif j == 0:
                #results.append('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX&page=1')
                #j += 1
            for y in results:
                page_url = y
                #print page_url
                yield Request(page_url, callback=self.parse_next_page)

    def parse_next_page(self, response):
        company_url = response.xpath('//a[@title="View detailed prices page"]/@href').extract()
        company_name = response.xpath('//a[@title="View detailed prices page"]/text()').extract()
        company_code = response.xpath('//td[@scope="row"]/text()').extract()
        n = 0
        for e in company_name:
            item = FtseItem()
            item['company_url'] = 'http://www.londonstockexchange.com' + company_url[n]
            item['company_name'] = company_name[n]
            item['company_code'] = company_code[n]
            item['count'] = n
            n += 1
            #yield item
            yield Request(item['company_url'], callback=self.parse_company, meta=dict(item=item))


    def parse_company(self, response):
        item = response.meta['item']
        item['company_address'] = response.xpath('//table[@summary="Company Information"]//tr[1]/td[2]/text()').extract()
        item['company_website'] = response.xpath('//table[@summary="Company Information"]//tr[2]/td[2]/a/@href').extract()
        company_website = response.xpath('//table[@summary="Company Information"]//tr[2]/td[2]/a/@href').extract()
        #test whether address contains London
        if re.match('^.*?(l?L?ondon).*?$', item['company_address'][0]):
            #yield item
            yield Request(company_website[0], callback=self.parse_website, meta=dict(item=item))
            #save work so far into spreadsheet: scrapy crawl ftse1 -o ftse_companies1.csv


    #gather contact information
    def parse_website(self, response):
        item = response.meta['item']
        get_website = response #this gets us current URL crawling!
        website = re.match('<200\s*(.*?)>', str(get_website)).group(1)
        #print website
        item['company_url'] = website
        #company_url = item['company_url'][0]
        
        
        #print Request(company_website[0], callback=self.parse_website)
        ###test to get current company_url###
        #1
        #if response.xpath('//link[@rel="canonical"]/@href').extract():
            #item['company_url'] = response.xpath('//link[@rel="canonical"]/@href').extract()
            #url = response.xpath('//link[@rel="canonical"]/@href').extract()[0] #working
        #elif response.xpath('//meta[@id="meta-url"]').extract():
            #content = response.xpath('//meta[@id="meta-url"]').extract()
            #website = re.match('.*content="(.*?)".*', content[0]).group(1)
            #item['company_url'] = website
        #else:
            #"TEST"  
        #elif :
            #item['company_url'] = 
        #else :
            #item['company_url'] = 

  

        #create URL for company contacts
        links = response.xpath('//a/@href').extract()
        x = 0
        #while not re.match('.*((?:a|A)bout\s*-?\s*(?:u|U)s).*', links[x]): #this works!
        
        while not re.match('.*((?:W|w)ho\s*-?_?\s*(?:W|w)e\s*-?_?\s*(?:A|a)re|(?:A|a)bout\s*-?_?\s*(?:U|u)s|(?:A|a)bout|(?:C|c)ontact\s*-?_?\s*(?:directory|(?:U|u)s)?).*', links[x]):
            x += 1
        test_url = website + links[x]
        #print test_url   #test

        #test for errors: http://www.g4s.com



        #test for '/' at the end of company website
        if re.match('.*?\/\/.*?(\/\/).*', test_url):
            print "Yes, we have a match!"
            rep = re.match('.*?\/\/.*?(\/\/).*', test_url).group(1) #this works!
            #print rep    #test
            new_url = test_url.replace(rep,'/')
        else:
            new_url = test_url
        item['about_url'] = new_url  #yay! This works!
        #yield item
        yield Request(item['about_url'], callback=self.parse_contact_info, meta=dict(item=item))

    #get contact information
    #def parse_contact_info(self, response):
        #test_content = response.xpath('//text()').extract()

        
