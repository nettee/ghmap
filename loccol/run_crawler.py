#!/usr/bin/env python3

import scrapy
from scrapy.crawler import CrawlerProcess

from loccol.spiders.user_spider import UserSpider

if __name__ == '__main__':

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    })

    process.crawl(UserSpider)
    process.start()
