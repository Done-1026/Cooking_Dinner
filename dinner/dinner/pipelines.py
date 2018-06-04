# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem

class DinnerPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        if item['dish_id'] in self.ids_seen:
            raise DropItem("Duplicate item found:%s"%item)
        else:
            self.ids_seen.add(item['dish_id'])
            for k,v in item.items():
                if k != 'dish_id':
                    item[k] = ','.join(v)
            return item

class Sqlite3WritePipeline(object):

    def open_spider(self,spider):
        self.conn = sqlite3.connect(r'D:\study\dinner\dinner\origin_data\origin.db')
        self.curs = self.conn.cursor()

    def close_spider(self,spider):
        self.conn.commit()
        print('存储成功')
        self.conn.close()
        
    def process_item(self, item, spider):
        #values = tuple(item.values())
        try:
            self.curs.execute("INSERT INTO cookbook (dish_id,name,other,tags) VALUES (?,?,?,?)"
                          ,tuple(item.values()))
        except sqlite3.IntegrityError:
            raise DropItem("****%s,我们有这个菜了****"%item['name'])
        return item
     
    
