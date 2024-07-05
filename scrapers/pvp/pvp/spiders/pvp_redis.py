import scrapy
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException,NoSuchElementException
# for link extraction
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
# for regular expression
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from scrapy.http import HtmlResponse, Response
import json
import ast
import html_to_json
from http.client import HTTPResponse
from bs4 import BeautifulSoup
import scrapy
from scrapy_redis.spiders import RedisSpider
#from scrapy_seleniumbase import SeleniumbaseRequest
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys


class PvpRedisSpider(RedisSpider):
    name = "pvp_redis"
    redis_key = 'data_queue:pvp'
    uniqueemail = set()
    url = ""
    print(redis_key)
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 4

    def make_request_from_data(self, data):
        #convert data string using eval  to dictionary
        self.url = data.decode('utf-8')
        print(self.url)
        

        return scrapy.Request(url=self.url, dont_filter=True)
    

    def parse(self, response):
        product = {}
        #files 
        numero_inserzione = response.xpath('//h1/text()').getall()
        urls = response.xpath('//*[@class="info-row"]//a/@href').getall()
        websites = []
        file_urls = []
        for url in urls:
            if str(url).endswith('.pdf') or '.pdf' in str(url):
                file_urls.append(url)
            else:
                websites.append(url)
        product["websites"] = websites
        product['file_urls'] = ["https://pvp.giustizia.it"+url for url in file_urls]
       
        product['descrizione'] = response.xpath('//*[@id="annunci"]/div/div[1]/div[1]/div[2]/div/text()').get().strip()    
        product['numero_inserzione'] = numero_inserzione[1].replace('\r','').replace('\n','').replace('\t','').replace('Inserzione N.','').strip()
        rows = response.xpath('//*[@class="row"]')
        for e in rows:
            key = e.xpath('./div/text()').get()
            value = e.xpath('./div[2]//text()').getall()
            value = ' '.join(value).strip().replace('\n','')
            if key and value.strip() and key.lower().strip().replace(' ', '_') != '':
                product[key.lower().strip().replace(' ', '_')] = value.replace('\r','').replace('\t','')
        yield product
