import scrapy
import json
import time

from scrapy_redis.spiders import RedisSpider
from redis import Redis
from bs4 import BeautifulSoup

from dinner.items import DinnerItem



class CookbookSpider(RedisSpider):
    name = 'cookbook'
    allowed_domains = ['www.haodou.com']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
               #'Host':'www.haodou.com',
               #'Connection':'keep-alive',
               #'Referer': 'http://www.haodou.com/recipe/all/',
               #'Upgrade-Insecure-Requests': 1
               }
    start_urls = ["http://www.haodou.com/recipe/all/?do=getpage&type=1&total=1485&page=2"]

    def parse(self,response):
        '''获取最大页数，构建每页的url'''
        soup = BeautifulSoup(json.loads(response.text)['info'],'html.parser')
        totalpage = int(soup.find_all('a')[-2].text)
        print(totalpage)
        for bigpg in range(1,totalpage+1):
            for smallpg in range(1,4):
                url = "http://www.haodou.com/recipe/all/?do=getrecipe&tid=&order=\
time&bigpage="+ str(bigpg) +"&smallpage=" + str(smallpg)
                #末页的时候可能smallpage23无内容
                yield scrapy.Request(url,headers=self.headers,callback=self.parse_url)
                
                            
    def parse_url(self,response):
        '''获取每个菜的id，构建每个菜的url'''
        #print('开始')
        info = json.loads(response.text)['info']
        for i in info:
            meta={}
            meta['id'] = dish_id = i['id']
            url = "http://www.haodou.com/recipe/"+str(dish_id)+'/'
            yield scrapy.Request(url,headers=self.headers,meta=meta,callback=self.dishparse)

    def dishparse(self,response):
        item = DinnerItem()
        item['dish_id'] = response.meta['id']
        large_info = response.xpath("//div[@class='large_info']")
        item['name'] = large_info.xpath("./div[@class='box']/h1/text()").extract()
        item['tags'] = large_info.xpath("./div[contains(@class,'mgt20')]//a/text()").extract()
        item['other'] = large_info.xpath("./ul//li/text()").extract()
        yield item
        
        
        
        
            

    
