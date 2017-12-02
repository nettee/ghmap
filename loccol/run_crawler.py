#!/usr/bin/env python3

import click

import scrapy
from scrapy.crawler import CrawlerProcess

from loccol.spiders.user_spider import UserSpider

@click.command()
@click.argument('username')
@click.option('--user-count', default=10, help='Number of users to fetch')
@click.option('-o', '--output', default='out.json', help='Output JSON file')
def crawl(username, user_count, output):
            
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': output,
        'CLOSESPIDER_ITEMCOUNT': user_count,
    }

    kwargs = {
        'username': username,
    }

    process = CrawlerProcess(settings)
    process.crawl(UserSpider, **kwargs)
    process.start()

if __name__ == '__main__':
    crawl()
