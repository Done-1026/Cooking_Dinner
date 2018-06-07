import random
import threading
import json
import re
import time
import telnetlib

from bs4 import BeautifulSoup
import requests

#from dinner.user_agents import agents
from user_agents import agents
from proxies_urls import proxies_urls

class Proxies():

    def __init__(self):
        self.pool=set()
        self.get_xc_proxies()

    def create_soups(self,key):
        '''根据代理ip页面，创建soup列表'''
        soups = []
        url_info = proxies_urls.get(key,None)
        if url_info:
            for page in range(1,url_info['pages']+1):
                headers ={
                    'User-Agent':random.choice(agents),
                    }
                url = url_info['url'] + url_info['type'] + str(page)
                resp = requests.get(url,headers=headers)
                soups.append(BeautifulSoup(resp.content,'html.parser'))
            return soups
        else:
            raise KeyError("Non-existent!")

    def get_xc_proxies(self):
        '''创建线程，每个线程都对一个soup进行解析与清洗'''
        soups = self.create_soups('xc')
        tds = []
        self.stime = time.time()
        for soup in soups:
            self.get_xc_ip(soup)
        self.etime = time.time()
          

    def get_xc_ip(self,soup):
        '''ip地址的抓取及验证，存入ips'''
        tds = []
        for tr in soup.find_all('tr')[1:]:           
            ip = list(tr.stripped_strings)[:2]
            td = threading.Thread(target=self.check_save_ip,args=(ip,))
            tds.append(td)
        for i in tds:
            i.start()
        for i in tds:
            i.join()
             
    def check_save_ip(self,ip):
        '''对ip进行验证'''
        #TODO:使用ip进行连接，判定是否可用，设定timeout
        try:
            telnetlib.Telnet(ip[0],ip[1],timeout=2)
            print(ip)
            self.pool.add(':'.join(ip))
            
        except:
            print('connet error,drop ip.')
            
        

if __name__ == '__main__':
    a = Proxies()
    print(a.etime-a.stime)

