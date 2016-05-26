# -*- coding: utf-8 -*-

import scrapy
import re
import requests
import urllib2
import codecs
import sys #try this
import json
from pyquery import PyQuery as pq
from lxml import etree
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from oxygendemo.items import OxygendemoItem

class OxygendemoSpider(CrawlSpider):
    name = "oxygenboutique.com"
    #allowed_domains = ["londonstockexchange.com",".*"]
    handle_httpstatus_list = [404]

    #put in two start URLs:
    #1 http://www.oxygenboutique.com/clothing.aspx
    #2 http://www.oxygenboutique.com/Sale-In.aspx


                

    #experiment with different start URLs
    def start_requests(self):
        url_list = ['http://www.oxygenboutique.com/clothing.aspx','http://www.oxygenboutique.com/Shoes-All.aspx','http://www.oxygenboutique.com/accessories-all.aspx','http://www.oxygenboutique.com/Sale-In.aspx']
        for link in url_list:
            init_url = link
            yield Request(init_url, callback=self.parse_pages)

    def parse_pages(self, response):
        #get current url
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        response = requests.get(url)
        doc = pq(response.content)
        #create page URLs
        #get number of last page
        pages = [e.text for e in doc('span.pg_total')]
        pages = pages[0].replace(re.match('.*?(\s{2,}).*', pages[0]).group(1),'')
        max_page = re.match('\d+of(\d+).*', pages).group(1)
        
        
        #make next page
        max_page = int(max_page)
        k = 1
        next_pages = []
        while k <= max_page:
            next_page = str(url) + '?pNo=' + str(k)
            next_pages.append(next_page)
            k += 1
            #nice list ['http://www.oxygenboutique.com/clothing.aspx?pNo=1', 'http://www.oxygenboutique.com/clothing.aspx?pNo=2']
            #loop through list
            for e in next_pages:
                next_page = e
                yield Request(next_page, callback=self.parse_next_page)

                

    def parse_next_page(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        response = requests.get(url)
        doc = pq(response.content)
        codes = []
        links = []
        prices = []
        i = 0
        for link in doc('div.itm a'):
            el = link.attrib['href']
            #get rid of '.aspx'
            code = el.replace(re.match('.*?(\.aspx.*$)', str(el)).group(1), '')
            url = 'http://www.oxygenboutique.com/' + el
            if code in codes:
                x = code
            else:
                codes.append(code)
                links.append(url)
                
        #test for reduction
        #get contents of page like so...
        #contents = doc('div.DataContainer')
        #reductions = []
        #for e in contents:
            #if re.match('.*?(\d+\.\d+)<.*', doc('span span span span')):
                #reduction = re.match('.*?(\d+\.\d+)<.*', doc('span span span span')).group(1)
                #reductions.append(reduction)
            #else:
                #reduction = 'None'
                #reductions.append(reduction)

        
        #print "this is the length of the list: " + str(len(codes)) #for testing

        while i < len(codes):
            item = OxygendemoItem()
            item['code'] = codes[i]  #1
            item['link'] = links[i]  #2
            #item['sale_discount'] = reductions[i]
            #item['gbp_price'] = prices[i]
            #yield item #for testing
            i += 1
            yield Request(item['link'], callback=self.parse_item_page, meta=dict(item=item))
            


    def parse_item_page(self, response):
        item = response.meta['item']
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
        response = requests.get(url)
        doc = pq(response.content)

        #test for 'Sale-In' URL
        #if not re.match('.*?Sale-In.*', url):
        test = [e.text for e in doc('span.offsetMark')]
        test = test[0].strip()
        if test == '':
            sale_discount = 'None'
            #get price data
        
            raw_price = [e.text for e in doc('span.price.geo_16_darkbrown')]  #test this on diff pages
            for f in raw_price:
                elem1 = f
                elem2 = elem1.strip()

            pounds = elem2.encode('raw_unicode_escape')
            num = re.match('.*?(\d+\.\d+).*', pounds).group(1) #works!
            num = float(num)  #works!
            #convert to $
            dollars = float(1.50 * num)
            dollars = str(dollars)
        
            #convert to €
            euros = float(1.37 * num)
            euros = str(euros)

            mark1 = euros.find('.')
            mark2 = dollars.find('.')


            euros2 = euros[mark1+1:]
            dollars2 = dollars[mark2+1:]
            #format '€' symbol
            euro = '€'.decode('utf-8')
            euro = euro.encode('raw_unicode_escape')


            if len(euros2) < 2:
                euros = euro + str(euros) + str(0)
            elif len(euros2) > 2:
                euros = euro + str(euros)[:mark1] + str(euros)[mark1:mark1+3]
            else:
                euros = euro + str(euros)

            if len(dollars2) < 2:
                dollars = '$' + str(dollars) + str(0)
            elif len(usd2) > 2:
                dollars = '$' + str(dollars)[:mark2] + str(dollars)[mark2:mark2+3]
            else:
                dollars = '$' + str(dollars)


        else:
            #get reduced and full prices
            triplets = [e.text for e in doc('span.price.geo_16_darkbrown span')]
            pairs = []

            for e in triplets:
                if e is None:
                    x = e
                else:
                    e.strip()
                    pairs.append(e)


            sale_discount = pairs[1].strip()
            
            #format '£' symbol
            pound = '£'.decode('utf-8')
            pound = pound.encode('raw_unicode_escape')
            pounds = pound + str(pairs[0].strip())
            sale_discount = pound + sale_discount
            num = float(pairs[0].strip())
            #convert to $
            dollars = float(1.50 * num)
            dollars = round(dollars,2)
            dollars = '$' + str(dollars)
        
            #convert to €
            euros = float(1.37 * num)
            euros = round(euros,2)
            #format '€' symbol
            euro = '€'.decode('utf-8')
            euro = euro.encode('raw_unicode_escape')
            euros = euro + str(euros)


            

        #get images
        imgs = []
        for e in doc('div#product-images a'):
            img = e.attrib['href']
            imgs.append(img)
            #print imgs  #test

        #test for duplicates
        test = []
        unique = []
        for e in imgs:
            if e in test:
		x = e
            else:
                test.append(e)
		pic = 'http://www.oxygenboutique.com' + e
		unique.append(pic)
        item['images'] = unique     #3


        name = [e.text for e in doc('div.right h2')]
        for e in name:
            name2 = e.strip(re.match('(^\r\n\s+).*',e).group(1))
        item['name'] = name2    #4

        #get description
        text = [g.text for g in doc('div')]
        #clean the text, to get just description
        description = ''
        for e in text:
            if e is None:
                x = e
            elif re.match('\s+BAG\s*.\s+', e):
                x = e
            elif re.match('\s*[a-zA-Z0-9,.]+\s*\n*', e):
                description = description + " " + e + "."
            elif re.match('\s*\n+\s*', e):
                x = e
            elif re.match('\s+', e):
                x = e
            else:
                x = e



        description = description.strip()
        if re.match('.*?(\s{2,}).*', description):
            description = description.replace(re.match('.*?(\s{2,}).*', description).group(1),'')
        if re.match('.*?(\s{2,}).*', description):
            description = description.replace(re.match('.*?(\s{2,}).*', description).group(1),'')
        if re.match('.*?(\s*\n+\s*).*', description):
            description = description.replace(re.match('.*?(\s*\n+\s*).*', description).group(1),'')
        if re.match('.*?(\.?\s*:\s*\.?\s*).*', description):
            description = description.replace(re.match('.*?(\.?\s*:\s*\.?\s*).*', description).group(1),'. ')
        if re.match('.*?(\.{2,}|\.\s{2,}|\s{2,}).*', description):
            description = description.replace(re.match('.*?(\.{2,}|\.\s{2,}|\s{2,}).*', description).group(1),'.')
        description = description.encode('raw_unicode_escape')

        

        edit = [e.text for e in doc('a#ctl00_ContentPlaceHolder1_AnchorDesigner')]  #get designer
        designer = edit[0].strip()

        
        #get gender  -  default to female [website only has women's cloths]
        
        #get raw_color - use description to determine this
        text1 = name2.lower()
        text2 = description.lower()


        if re.match('.*?\s(red|blue|green|orange|pink|purple|brown|white|black|grey|yellow|gold|silver|turqoise|maroon)\s*.*', text1):
            color = re.match('.*?\s(red|blue|green|orange|pink|purple|brown|white|black|grey|yellow|gold|silver|turqoise|maroon)\s*.*', text1).group(1)
            #print "name2: " + color  #test

        elif re.match('.*?\s(red|blue|green|orange|pink|purple|brown|white|black|grey|yellow|gold|silver|turqoise|maroon)\s*.*', text2):
            color = re.match('.*?\s(red|blue|green|orange|pink|purple|brown|white|black|grey|yellow|gold|silver|turqoise|maroon)\s*.*', text2).group(1)
            #print "description: " + color  #test

        else:
            color = 'None'
            #print color  #test


 
                

        
        #return 'None' if unidentifiable

        #stock_status - dictionary of sizes to stock status
        #1 - out of stock
        #3 - in stock
        #i.e. 'stock_status': {'L': 1, 'M': 1, 'S': 1, 'XS': 1},

        options = doc('option')
        sizes = []
        for e in options:
            size = e.text
            if re.match('.*?((?:P|p)lease\s*(?:S|s)elect).*', size):
                x = size
            elif re.match('.*?((?:S|s)old\s*(?:O|o)ut).*', size):
                sizes.append(size)
            else:
                size = size + " - Available"
                sizes.append(size)


        #clothing_type
        #match one of:
        stuff = [e.text for e in doc('h2')]
        title = stuff[0].strip()
        title = title.lower()



        #'A' apparel
        if re.match('.*?(bra|tee|skirt|shirt|t\s*-?\s*shirt|vest|dress|pyjamas|trousers|shorts|suit|top|denim|bottoms?|all\s*-?\s*in\s*-?\s*ones|outerwear|cardigans|beachwear|sportswear|lingerie).*', title):
            clothing_type = 'A'
        #'S' shoes
        elif re.match('.*?(shoe|boot|sandal|slipper|flip\s*-?\s*flop|trainer|sneaker|lace\s*-?\s*up|heels?|flats?|wedges?).*', title):
            clothing_type = 'S'  
        #'B' bags
        elif re.match('.*?(bag|brief\s*-?\s*case|ruck\s*-?sack|satchel).*', title):
            clothing_type = 'B'
        #'J' jewelry
        elif re.match('.*?(ring|necklace|ear\s*-?\s*ring|brooch|pendant|choker|bracelet).*', title):
            clothing_type = 'J'
        #'R' accessories
        elif re.match('.*?(hats?|iphone\s*cases?|homewear|tattoos?|crystal\s*tattoos?).*', title):
            clothing_type = 'R'
        else:
            clothing_type = 'None'

        item['usd_price'] = dollars  #5
        item['eur_price'] = euros    #6
        item['gbp_price'] = pounds   #7
        item['designer'] = designer  #8
        item['description'] = description  #9
        item['gender'] = 'F'  #10
        item['raw_color'] = color  #11
        item['stock_status'] = sizes #12
        item['clothing_type'] = clothing_type  #13
        item['sale_discount'] = sale_discount  #14  #only applies to http://www.oxygenboutique.com/Sale-In.aspx
        yield item
            
        #scrapy crawl oxygenboutique.com -o items.csv
        #scrapy crawl oxygenboutique.com -o items.json


#Seraphina Anderson, Oxygen Crawler, 18/12/15
        
