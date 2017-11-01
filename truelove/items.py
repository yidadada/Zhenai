# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import redis

class TrueloveItem(scrapy.Item):
    username = scrapy.Field()
    userage = scrapy.Field()
    userheight = scrapy.Field()
    #userselary = scrapy.Field()
    age = scrapy.Field()
    usereducation = scrapy.Field()

