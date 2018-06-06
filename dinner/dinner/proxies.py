import random
import threading
import json

from bs4 import BeautifulSoup
import requests

#from dinner.user_agents import agents
from user_agents import agents
from proxies_urls import proxies_urls

class Proxies():

    def __init__(self):
        self.ips = set()
        self.urls = proxies_urls
        self.get_xc_proxies()

    def create_soups(self,key):
        soups = []
        url_info = self.urls.get(key,None)
        if url_info:
            for page in range(1,url_info['pages']+1):
                headers ={
                    'User-Agent':random.choice(agents),
                    }
                url = url_info['url'] + str(page)
                resp = requests.get(url,headers=headers)
                soups.append(BeautifulSoup(resp.content,'html.parser'))
            return soups
        else:
            raise KeyError("Non-existent!")

    def get_xc_proxies(self):
        soups = self.create_soups('xc')
        for soup in soups:
            td = threading.Thread(target=self.get_xc_ip,args=(soup,))
            td.start()

    def get_xc_ip(self,soup):
        for tr in soup.find_all('tr')[1:]:
            ip = ':'.join(list(tr.stripped_strings)[:2])
            self.ips.add(ip)

a = Proxies()

