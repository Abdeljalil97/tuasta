from typing import Iterable
import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import Request
#from scrapy_seleniumbase import SeleniumbaseRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
import time
import redis
redisClient = redis.from_url('redis://127.0.0.1:6379')
# driver = Driver(undetectable=True, uc_cdp_events=True,chromium_arg="log-level=3,disable-logging",headless=False)
# driver.maximize_window()


class SpiderSpider(scrapy.Spider):
    
    
    name = "quimmo"
    categories = []

    def start_requests(self) :
        urls = ["https://www.quimmo.it/procedure","https://www.quimmo.it/annunci-immobili",
                "https://www.quimmo.it/vendita-immobili/capannoni",
                "https://www.quimmo.it/vendita-immobili/case",
                "https://www.quimmo.it/vendita-immobili/edifici",
                "https://www.quimmo.it/vendita-immobili/impianti-sportivi",
                "https://www.quimmo.it/vendita-immobili/locali-commerciali",
                "https://www.quimmo.it/vendita-immobili/parcheggi",
                "https://www.quimmo.it/vendita-immobili/sanitario-assistenziali",
                "https://www.quimmo.it/vendita-immobili/strutture-ricettive",
                "https://www.quimmo.it/vendita-immobili/terreni",
                "https://www.quimmo.it/vendita-immobili/uffici"
                ]
        for url in urls :
            yield scrapy.Request(url=url,callback=self.get_listing)
   

    def get_listing(self,response):
        number_of_page = response.xpath("""//*[@aria-label="Vai all'ultima pagina"]/@href""").get()
        if number_of_page:
            number_of_page = number_of_page.split('pag=')[1].strip()
        print(number_of_page)   
             
        if  number_of_page:
            for i in range(1,int(number_of_page)):
                url = response.url+f"?pag={i}"
                yield scrapy.Request(url=url,callback=self.push_to_redis)
        else :
            yield scrapy.Request(url=response.url+"?pag=2",callback=self.push_to_redis)


    def push_to_redis(self,response):
        links = response.xpath('//h4/a/@href').getall()
        print(len(links))
        print(links)
        for link in links:
            if "https:" not in link :
                redisClient.lpush('data_queue:quimmo', "https://www.quimmo.it"+link)
            else :
                redisClient.lpush('data_queue:quimmo', link)
        
