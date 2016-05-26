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
from twitterscape.items import TwitterscapeItem

#Info: broad crawler for searching and harvesting sample twitter usernames, given
#some keywords as starting point


class TwitterUsers(CrawlSpider):
    name = "usernames"
   
    #create list of keywords, and loop through searches here
    def start_requests(self):
        urls = ['https://twitter.com/hashtag/unhappy', 'https://twitter.com/hashtag/weird',
                'https://twitter.com/hashtag/beautiful', 'https://twitter.com/hashtag/angry']
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_Url)
            i += 1


    def parse_Url(self, response):
        #Collect Twitter User Names here!
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1) #Get current scrape URL
        
        user = response.xpath('*//a').re('.*?data-mentioned-user-id.*')
        username = ['@' + re.match('.*?<b>(.*?)</b>.*', e).group(1) for e in user if re.match('.*?<b>(.*?)</b>.*', e)]
        userid = 
        j = 0
        while j < len(user):
            item = TwitterscapeItem()
            item['userNumber'] = j + 1
            item['userName'] = username[j]
            item['userStatus'] = 1
            item['userID'] = userid[j]
            yield item
            j += 1



    #Transfer info to .csv file: scrapy crawl usernames -o usernames.csv

        

            

    


