#!/usr/bin/env python3

import os

import click

import scrapy
from scrapy.crawler import CrawlerProcess

from loccol.spiders.user import UserSpider

@click.command()
@click.argument('username')
@click.option('--max-order', default=6, help='Max order of your followers')
@click.option('--max-user', default=500, help='Max number of users')
@click.option('-o', '--output', default='out.json', help='Output JSON file')
def crawl(username, max_order, max_user, output):
            
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': output,
        'CLOSESPIDER_ITEMCOUNT': max_user,
    }

    kwargs = {
        'username': username,
        'max_order': max_order,
    }

    if os.path.exists(output):
        os.remove(output)

    process = CrawlerProcess(settings)
    process.crawl(UserSpider, **kwargs)
    process.start()

if __name__ == '__main__':
    crawl()
