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
from scrapy_seleniumbase import SeleniumbaseRequest
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
import time

class QuiRedisSpider(RedisSpider):
    name = "qui_redis"
    redis_key = 'data_queue:quimmo'
    uniqueemail = set()
    url = ""
    print(redis_key)
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 7200

    def make_request_from_data(self, data):
        #convert data string using eval  to dictionary
        self.url = data.decode('utf-8')
        print(self.url)
        

        return SeleniumbaseRequest(url=self.url, dont_filter=True)
    

    def parse(self, response):

        driver = response.request.meta['driver']

        cheek = str(response.url).replace('https://www.quimmo.it/','').split('/')
        if len(cheek) > 1:
            driver.get(response.url)
            driver.maximize_window()
            body = str.encode(driver.page_source)
            new_response = HtmlResponse(
                driver.current_url,
                body=body,
                encoding='utf-8',
                
            )
            
            try:
            
                Chiudi = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, '//*[@title="Chiudi"]'))
                                )
                Chiudi.click()
            except TimeoutException:
                pass
            for i in range(1,6):
                html = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.TAG_NAME, "html"))
                            )
                #html.click()
                
                print(f"\033[0;35m\U0001F6A7 Job \033[1;32m Scrolling to download fields")
                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            product = {}
            product['numero_inserzione'] = new_response.url.split('-')[len(new_response.url.split('-'))-1]
            title = new_response.xpath('//h1/text()').get()
            price = new_response.xpath('//*[@class="q-price"]/p/text()').get()
            images_urls = new_response.xpath('//img[@class="mds-image"]/@src').getall()
            try:
                poi__category = WebDriverWait(driver, 20).until(
                                    EC.presence_of_all_elements_located((By.XPATH, '//*[@class="poi__category"]'))
                                )
                for c in poi__category:
                    h= {}
                    eles = c.find_elements(By.XPATH, './/li')
                    for e in eles:
                        h[f"""{e.find_element(By.XPATH,'.//*[@class="poi__name"]').text}"""] = e.find_element(By.XPATH,'.//*[@class="poi__distance"]').text
                    product[f"{c.find_element(By.XPATH, './/strong').text}"] = h
            except TimeoutException:
                pass
            try :
                iframe = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, '//iframe[@class="location__google-map-iframe"]'))
                                )

                
                driver.switch_to.frame(iframe)
                #google_maps = response.xpath('/@href').get()
                google_maps = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, '//*[@class="navigate"]/a'))
                                )
                google_maps=google_maps.get_attribute('href')
                driver.switch_to.default_content()
            except TimeoutException:
                pass
            product['images_urls'] = images_urls
            try:
                product['google_maps'] = google_maps
            except:
                pass

            product["title"] = title
            product['price'] = price
            #
            description = new_response.xpath('//*[@class="description__text description__text--truncated"]//text()').getall()
            description = ' '.join(description).strip().replace('\n','')
            product['descrizione'] = description
            elements = new_response.xpath('//*[@class="detail-container-with-label"]')
            for e in elements:
                key = e.xpath('./p[1]/text()').get()
                print(key)
                value = e.xpath('./p[2]/text()').get()
                if key and value :
                    product[key.strip().lower().replace(' ', '_')] = value.strip()
            yield product
        else:
            print(response.url) 
    

    

