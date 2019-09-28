#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


# In[2]:


class UserAgent():
    
    def __init__(self, url="http://www.useragentstring.com/pages/useragentstring.php?name=All"):
        self.url = url
        self.list = []
    def get_list(self):
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        time.sleep(6)
        page_soup = BeautifulSoup(response.content, "html.parser")
        search = page_soup.findAll("a")
        for i in range(5,len(search) - 2):
            if "/" in search[i].text:
                self.list.append(search[i].text)
        return self.list


# In[3]:


class Ip():
    
    def __init__(self, url="https://free-proxy-list.net/"):
        self.url = url
        self.list = []
    def get_ip(self):
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        time.sleep(6)
        page_soup = BeautifulSoup(response.content, "html.parser")
        search = page_soup.findAll("tr")
        search_want = search[1:301]
        for tr in search_want:
            tdd = tr.findAll("td")
            if tdd[-2].text == "yes":
                if tdd[4].text == "elite proxy":
                    value =  "https://" + tdd[0].text + ":" + tdd[1].text
                    self.list.append(value)
            else:
                continue
        return self.list
        

        
        
        
        
    


# In[ ]:




