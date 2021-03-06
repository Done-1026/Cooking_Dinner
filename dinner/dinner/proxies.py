import random
import threading
import time
import telnetlib
import json

from bs4 import BeautifulSoup
import requests

# from dinner.user_agents import agents
from dinner.info import AGENTS,URLS


class Proxies():

    def __init__(self):
        #self.stime = time.time()
        self.refresh_pool()
        #self.etime = time.time()

    def create_soups(self, key):
        '''根据代理ip页面，创建soup列表'''
        soups = []
        url_info = URLS.get(key, None)
        if url_info:
            for page in range(1, url_info['pages'] + 1):
                headers = {
                    'User-Agent': random.choice(AGENTS),
                }
                url = url_info['url'] + url_info['type'] + str(page)
                resp = requests.get(url, headers=headers)
                soups.append(BeautifulSoup(resp.content, 'html.parser'))
            return soups
        else:
            raise KeyError("Non-existent!")

    def get_xc_ip(self):
        for soup in self.create_soups('xc'):
            for tr in soup.find_all('tr')[1:]:
                ip = list(tr.stripped_strings)[:2]
                td = threading.Thread(target=self.check_save_ip, args=(ip,))
                self.threads.append(td)

    def get_pool(self):
        for i in self.threads:
            i.start()
        for i in self.threads:
            i.join()

    def check_save_ip(self, ip):
        '''ip地址的抓取及验证，存入ips'''
        try:
            telnetlib.Telnet(ip[0], ip[1], timeout=2)
            print(ip)
            self.pool.add(':'.join(ip))
        except:
            #print('connet error,drop ip.')
            pass

    def refresh_pool(self):
        self.threads = []
        self.pool = set()
        self.get_xc_ip()

        self.get_pool()
        
        
        


