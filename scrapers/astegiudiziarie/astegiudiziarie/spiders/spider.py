from http.client import HTTPResponse
from bs4 import BeautifulSoup
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_seleniumbase import SeleniumbaseRequest
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
import re

def normalize_space(text):
    if text:
        # Remove leading and trailing whitespace
        text = text.strip()
        # Replace multiple spaces and newlines with a single space
        text = re.sub(r'\s+', ' ', text)
    return text

class SpiderSpider(RedisSpider):
    name = "astegiudiziarie"
    redis_key = 'data_queue:data'
    uniqueemail = set()
    url = ""
    print(redis_key)
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 3

    def make_request_from_data(self, data):
        #convert data string using eval  to dictionary
        self.url = data.decode('utf-8')
        data = json.loads(self.url)
        

        

        
        
        #input("Press Enter to continue...")
        return SeleniumbaseRequest(url=data['url'], dont_filter=True, meta = {'data': data})
    def parse(self, response) :
        d = response.meta['data']
        driver = response.request.meta['driver']
        driver.quit()
        product = {}

        d =response.meta['data']
        elements1 = response.xpath('//*[@class="col-sm-4 col-xs-6 col-xxs-12 light"]')
        elements2 = response.xpath('//*[@class="col-sm-4 col-xs-6 col-xxs-12 dark"]')
       
        for e in elements2:
            key = e.xpath('./div/text()').get().lower().strip().replace(' ', '_')
            value = e.xpath('./div[2]//text()').getall()
            value = ' '.join(value).strip().replace('\n','').replace('\t','').replace('\r','').replace('\xa0','')
            product[key] = normalize_space(value)
        for e in elements1:
            key = e.xpath('./div/text()').get().lower().strip().replace(' ', '_')
            value = e.xpath('./div[2]//text()').getall()
            value = ' '.join(value).strip().replace('\n','').replace('\t','').replace('\r','').replace('\xa0','')
            product[key] = normalize_space(value)
        images = response.xpath('//img/@src').getall()
        product['image_urls'] = [
    "https://astegiudiziarie.it" + img
    for img in images
    if img.startswith("/") and not img.startswith("/images") and not img.startswith("http") and not img.startswith("data")
]
        google_maps = response.xpath('//*[@id="propertyMap-container"]/a[text()="Google Maps"]/@onclick').get()
        if google_maps:
            google_maps = google_maps.split(";")
            google_maps = google_maps[len(google_maps)-1]
            # Define a regex pattern to match URLs
            pattern = r"(https?://[^\s]+)"
            # Use re.findall() to extract all URLs from the string re.findall(pattern, google_maps)
            product['google_maps'] =  google_maps.replace('popupCenter(','').replace(')','').replace('"','')
        #product['numero_inserzione'] = int(response.xpath("//*[contains(normalize-space(text()), 'COD')]/text()").get().replace('COD','').replace('.','').strip()) #html
        product['numero_inserzione'] = int(response.xpath('//*[@class="title-bar-auction-left"]/text()').get().replace('COD','').replace('.','').strip())
#//*[@class="title-bar-auction-left"]/text()
        product['offerta_minima'] = normalize_space(response.xpath('//*[@class="sub-price"]/text()').get())
        product['dettaglio_lotto'] = normalize_space(response.xpath('//*[@class="property-title"]/h2/text()').get())
        attachements = response.xpath('//*[@class="sidebar-attachment button"]/@href').getall()
        product['file_urls'] = [ "https://astegiudiziarie.it"+a for a in attachements]
        if product['image_urls']:
            for p in product['image_urls']:
                product['file_urls'].append(p)
        vendita = response.xpath('//*[@id="table-container"]/table').get()
        print("data:",vendita)
        if vendita:
            tables = html_to_json.convert_tables(vendita)
            product['data'] = tables
        yield product
        
            
    
      
