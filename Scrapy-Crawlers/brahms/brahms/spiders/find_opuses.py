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
from brahms.items import BrahmsItem



class Opuses(CrawlSpider):
    name = "brahms"

    def start_requests(self):
        url  = 'https://en.wikipedia.org/wiki/List_of_compositions_by_Johannes_Brahms_by_opus_number'
        yield Request(url, callback=self.parse_opuses)

    #Collect Opuses
    def parse_opuses(self, response):
        #item = BrahmsItem()
        get_url = response #this gets us current URL crawling!
        brahms_url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        #Should be 122 opuses
        opus = response.xpath('//li').re('.*?<b>Op\..*')
        opus_numbers = [re.match('.*?<b>Op\.\s*(.*?)<\/b>.*', e).group(1) if re.match('.*?<b>Op\.\s*(.*?)<\/b>.*', e) else e for e in opus]
        opus_names = [re.match('.*?title="(.*)\s*\n*\(Brahms\).*', e).group(1) if re.match('.*?title="(.*)\s*\n*\(Brahms\).*', e) else re.match('.*\n*.*?<b>Op\..*?<\/b>\n*"?\s*,?\s*(.*)"?', e).group(1) for e in opus]
        clean_names = [e.replace(re.match('<i><a.*?title=".*?>', e).group(0), '') if re.match('<i><a.*?title=".*?>', e) else e for e in opus_names]
        clean_names = [e.replace(re.match('(<a href=".*?">).*', e).group(1),'') if re.match('(<a href=".*?">).*', e) else e for e in clean_names]
        clean_names = [e.replace('</a>','') for e in clean_names]
        clean_names = [e.replace('</i>','') for e in clean_names]
        clean_names = [e.replace('<i>','') for e in clean_names]
        clean_names = [e.replace('</li>','') for e in clean_names]
        clean_names = [e.replace(re.match('.*?(<a href=.*?>).*',e).group(1),'') if re.match('.*?(<a href=.*?>).*',e) else e for e in clean_names]
        #print "length of names: ",len(clean_names), "length of opus numbers: ",len(opus_numbers)
        for i, f in enumerate(clean_names):
            #item['opus_name'] = clean_names[i]
            opus_number = opus_numbers[i]
            #item['opus_number'] = opus_number
            # get search URL
            search_url = 'https://www.youtube.com/results?search_query=brahms+Opus+' + str(opus_number)
            yield Request(search_url, callback=self.parse_search)


    def parse_search(self, response):
        item = BrahmsItem()
        #item = response.meta['item']
        get_url = response # this gets us current URL crawling!
        brahms_url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        #get num
        num = re.match('.*?brahms\+Opus\+(\d+\w*)', brahms_url).group(1)
        
        #print "testing #1: " + str(brahms_url)
        
        # generate YouTube Opus URL
        results = response.xpath('//ol[@class="item-section"]//div[@class="yt-lockup-content"]').extract()

        ###get relevant content###
        get_valid_results = [e for e in results if re.match('.*?title=.*?(?:O|o)(?:P|p)\.\s*(\d+\w*)[^0-9].*<li>\d+,?\d*\s*views<\/li>.*', e)]
        get_opus_num_results = [e for e in get_valid_results if re.match('.*?(?:O|o)(?:P|p)\.\s*(\d+\w*)[^0-9].*', e).group(1) == num]
        get_titles = [re.match('.*?(title=".*(?:O|o)(?:P|p)?\..*?").*', e).group(1) for e in get_opus_num_results if re.match('.*?(title=".*(?:O|o)(?:P|p)\..*?").*', e)]
        get_nums = [re.match('.*?(?:O|o)(?:P|p)\.\s*(\d+\w*)[^0-9].*', e).group(1) if re.match('.*?(?:O|o)(?:P|p)\.\s*(\d+\w*)[^0-9].*', e) else e for e in get_opus_num_results]

        get_views = [re.match('.*?<li>(\d+,?\d*)\s*views<\/li>.*', e).group(1) for e in get_opus_num_results if re.match('.*?<li>(\d+,?\d*)\s*views</li>.*', e)]
        int_views = [int(e.replace(',','')) for e in get_views]

        # get links
        youtube_links = ["https://www.youtube.com" + re.match('.*?href="(\/watch\?v=.*?)?".*',e).group(1) for e in get_opus_num_results]

        # find max views and associated link
        max_views = max(int_views)
        # get index of max views
        max_index = int_views.index(max_views)
        
        # collect link with largest number of views
        max_view_link = youtube_links[max_index]
        #print "testing #2: ", max_view_link

        # get link for next page
        nextpage = response.xpath('//a[@data-link-type="next"]/@href').extract()
        nextpage = 'https://www.youtube.com' + str(nextpage[0])

        item['opus_number'] = num
        
        yield Request(max_view_link, callback=self.parse_opus, meta=dict(item=item))


    def parse_opus(self, response):
        item = response.meta['item']
        #test url
        get_url = response # this gets us current URL crawling!
        youtube_url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        #print "testing #3: " + str(youtube_url)
        opus_name = response.xpath('//span[@class="watch-title"]/text()').extract()
        opus_name = opus_name[0].strip()
        item['opus_name'] = opus_name
        item['upvotes'] = response.xpath('//button[@title="I like this"]/span/text()').extract()
        item['views'] = response.xpath('//div[@class="watch-view-count"]/text()').re('\d+,?\d*')
        item['subscribed'] = response.xpath('//span[@class="yt-subscription-button-subscriber-count-branded-horizontal yt-short-subscriber-count"]/text()').extract()

        yield item

        
#Output: scrapy crawl brahms -o brahms1.csv
