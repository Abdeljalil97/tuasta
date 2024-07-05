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

class FaRedisSpider(RedisSpider):
    name = "fa_redis"
    redis_key = 'data_queue:fallcoaste'
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
        rows_data = []
        row_data = {}
        numero_inserzione = response.url.split('-')[len(response.url.split('-'))-1].replace('.html','')
        #//title
        row_data['title'] = response.xpath('//title/text()').get().strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # item = {}
        # item['numero_inserzione'] = numero_inserzione
        tables = response.xpath('//table').getall()
        # print(len(tables))
        

        
        # for t in tables:
        #     try:
        #         tables_data = html_to_json.convert_tables(t)
        #         print(tables_data)
        #         for table in tables_data:
        #             try:
        #                 keys_t = table.keys()
        #                 for k in keys_t:

        #                     rows_data[k.replace('\n','').strip().replace(' ','_')] = table[k].replace('\n','').strip()
        #             except AttributeError:
        #                 pass


                
        #     except IndexError :
        #         pass
        # yield item 
        # Initialize a list to store dictionaries
        
        row_data['numero_inserzione'] = numero_inserzione
        # Iterate over each table row
        for sel in response.xpath('//table//tr'):

            # Initialize a dictionary for each row
            

            # Extract key using the `th` element, taking all nested text elements into account
            key = ''.join(sel.xpath('.//th//text()').getall()).strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            
            # If the key exists, extract data from `td`
            if key:
                # Extract `td` value with nested tags support
                value = ''.join(sel.xpath('.//td//text()').getall()).strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                
                # Extract `href` attribute if present, usually for links
                link_or_email = sel.xpath('.//td/a/@href').get()
                if link_or_email and link_or_email != '#':
                    # Check if it is an email
                    if 'mailto:' in link_or_email:
                        value = link_or_email.split('mailto:', 1)[1]

                    # Otherwise, it's a link
                    else:
                        value = link_or_email
                        
                # Assign the value to the dictionary with the key
                row_data[key.replace(' ','_')] = value

                # Add the dictionary to the list of rows
        #rows_data.append(row_data)
        try:
            if row_data['Termine_presentazione_offerte:'] :
                pass
                #row_data['Termine_presentazione_offerte'] = row_data['-_con_Bonifico']
            else:
                row_data['Termine_presentazione_offerte:'] = row_data['-_con_Bonifico']
                pass
                
        except KeyError:
            pass
        files = response.xpath('//table//a/@href').getall()
        row_data['images_urls'] = response.xpath('//*[@id="auction-carousel"]/div[1]/div/div/figure/img/@data-src').getall()
        row_data['files_urls'] = []
        for f in files:
            if str(f).endswith('.pdf'):
                row_data['files_urls'].append(f)
        yield row_data

