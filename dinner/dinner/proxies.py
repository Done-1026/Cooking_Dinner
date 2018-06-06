import random
import json

from bs4 import BeautifulSoup
import requests

#from dinner.user_agents import agents
from user_agents import agents

class Proxies():

    https_proxy = []
    http_proxy = []

    urls = {
        'xc':{
            'url':"http://www.xicidaili.com/nn/",
            'pages':5,
            }
        }
       
    def create_soup(self,key):
        url_info = self.urls.get(key,None)
        if url_info:
            for page in range(url_info['pages']+1):
                headers ={
                    'User-Agent':random.choice(agents),
                    }
                url = url_info['url'] + str(page)
                resp = requests.get(url,headers=self.headers)
                soup = BeautifulSoup(resp.content,'html.parser')
        else:
            print("Non-existent!")

    def get_xc_proxies(self,soup):
        soup = self.create_soup('xc')
        tips = soup.find_all('tr')[0:]
        for tip in tips:
            if tip.find
        

        
    

    

a = Proxies()
soup = a.create_soup(a.url)
