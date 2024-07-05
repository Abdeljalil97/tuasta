import scrapy
import scrapy
from typing import Iterable
import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import Request
from scrapy_seleniumbase import SeleniumbaseRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import html_to_json
from seleniumbase import Driver
import time
import redis
redisClient = redis.from_url('redis://127.0.0.1:6379')
class SpiderSpider(scrapy.Spider):
    name = "fallcoaste"
    
    start_urls = []
    
    def start_requests(self):
        yield scrapy.Request(url="https://www.wikipedia.org/",callback=self.parse)

    def parse(self, response):
        #cheek_results = response.xpath('//*[text()="la ricerca non ha prodotto risultati"]').get()
        number_of_page = response.xpath('//b/text()').get()
        print(f"number of page {number_of_page} pages .")
        links_pagination = [f"https://www.fallcoaste.it/ricerca.html?page={i}" for i in range(1,686)]
        yield from response.follow_all(links_pagination, callback=self.get_all_links_products)
        
        # while True:
            
        

        
            
        #     links = response.xpath('//*[@class="search-result"]//a/@href').getall()
        #     urls = []
        #     for link in links :
        #         if str(link).endswith('.html') and link not in urls:
        #             urls.append(link)
        #     print(len(urls))
        #     print(urls)
        #     yield scrapy.Request(url=f"https://www.fallcoaste.it/ricerca.html?page={i}",callback=self.parse)
        #     i = i+1
           
    def get_all_links_products(self,response):
        links = response.xpath('//*[@class="search-result"]//a/@href').getall()
        urls = []
        for link in links:
            for link in links :
                if str(link).endswith('.html') and link not in urls:
                    urls.append(link)
        for url in urls :
            redisClient.lpush('data_queue:fallcoaste', url)
