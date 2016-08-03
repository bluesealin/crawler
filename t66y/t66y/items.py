# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy




class T66YItem(scrapy.Item):
    title = scrapy.Field()
    href=scrapy.Field()
    author=scrapy.Field()
    date_str=scrapy.Field()
    commentnum=scrapy.Field()
    content=scrapy.Field()

    
