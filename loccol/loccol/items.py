# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UserItem(scrapy.Item):
    username = scrapy.Field()
    order = scrapy.Field()
    linker = scrapy.Field()
    fullname = scrapy.Field()
    followers = scrapy.Field()
    location = scrapy.Field()
