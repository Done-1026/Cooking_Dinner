# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DinnerItem(scrapy.Item):
    dish_id = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    other = scrapy.Field()
    author = scrapy.Field()
    funs = scrapy.Field()
    summary = scrapy.Field()
    main_mate = scrapy.Field()
    assis_mate= scrapy.Field()
    procedure = scrapy.Field()
    
    
    
