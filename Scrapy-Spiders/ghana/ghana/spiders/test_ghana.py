import scrapy
#from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    start_urls = ["http://example.comhttp://yellowpages.com.gh/Search-Results.aspx?mcaid=1&eca1id=&eca2id=&eca3id=&eca4id=&eca5id=&lcaid=804#tabs-2", "http://yellowpages.com.gh/Search-Results.aspx?mcaid=1&eca1id=&eca2id=&eca3id=&eca4id=&eca5id=&lcaid=12#tabs-2"]
    name = "testghana"

    def process_links(self, start_urls):
        for link in links:
            link.url = "http://localhost:8050/render.html?" + urlencode({ 'url' : link.url })
        return links

    def parse(self, response):
        print "We made it!"
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # ...
