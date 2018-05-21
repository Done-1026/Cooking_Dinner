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
    makefor = scrapy.Field()
    author = scrapy.Field()
    funs = scrapy.Field()
    summary = scrapy.Field()
    main_material = scrapy.Field()
    assistant_material= scrapy.Field()
    
    
    
    
