# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from Bot_Scrap_Offre.items import BotScrapOffreItem

class FlashbotSpider(scrapy.Spider):
    name = 'flashbot'
    allowed_domains = ['rss.jobsearch.monster.com']

    # Start the crawler at this URLs
    #start_urls = ['file:///path/to/your/index.xml']
    start_urls = ['http://rss.jobsearch.monster.com/rssquery.ashx?q={query}']

    thesaurus = ["machine learning", "machine", "learning", "big data", "big", "data"]

    LOG_LEVEL = "INFO"

    def parse(self, response):
        # We stat with this url
        url = self.start_urls[0]

        # Build and send a request for each word of the thesaurus
        for query in self.thesaurus:
            target = url.format(query=query)
            print("fetching the URL: %s" % target)
            if target.startswith("file://"):
                r = Request(target, callback=self.scrapit, dont_filter=True)
            else:
                r = Request(target, callback=self.scrapit)
            r.meta['query'] = query
            yield r

    def scrapit(self, response):
        query = response.meta["query"]

        # Scrap the data
        for doc in response.xpath("//item"):
            item = BotScrapOffreItem(
                title = doc.xpath("title/text()").get(),
                description = doc.xpath("description/text()").get(),
                link = doc.xpath("link/text()").get(),
                pubDate = doc.xpath("pubDate/text()").get(),
                guid = doc.xpath("guid/text()").get(),
                query = query
                ) 
            yield item
