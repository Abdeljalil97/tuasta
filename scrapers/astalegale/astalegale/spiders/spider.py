import scrapy
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from scrapy_seleniumbase import SeleniumbaseRequest

import re

def extract_image_urls(html_content):
    """
    Extract all image links that start with 'https://documents.astalegale.net/images' from given HTML source code.

    :param html_content: HTML content as a string.
    :return: List of image URLs.
    """
    # Define the regex pattern to match URLs
    pattern = r"https://documents\.astalegale\.net/images[^\"'>\s]+"

    # Find all matches of the pattern
    matches = re.findall(pattern, html_content)

    # Remove potential duplicates by converting the list to a set and back to a list
    unique_matches = list(set(matches))

    return unique_matches
def extract_file_urls(html_content):
    """
    Extract all image links that start with 'https://documents.astalegale.net/file' from given HTML source code.

    :param html_content: HTML content as a string.
    :return: List of image URLs.
    """
    # Define the regex pattern to match URLs
    pattern = r"https://documents\.astalegale\.net/file[^\"'>\s]+"

    # Find all matches of the pattern
    matches = re.findall(pattern, html_content)

    # Remove potential duplicates by converting the list to a set and back to a list
    unique_matches = list(set(matches))

    return unique_matches

class SpiderSpider(RedisSpider):
    name = "astalegale"
    
    redis_key = 'data_queue:astalegale'
    uniqueemail = set()
    url = ""
    
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 10

    def make_request_from_data(self, data):
        #convert data string using eval  to dictionary
        self.url = data.decode('utf-8')
        
        

        return SeleniumbaseRequest(url=self.url, dont_filter=True)
    

    def parse(self, response):
        products = []
        product = {} 
        numero_inserzione = response.url.split('/')[len(response.url.split('/'))-1].split('-')[0]
        product['numero_inserzione'] = numero_inserzione
        
        #//*[@class="dettaglio_asta"]//*[@class="dettaglio_text"]
        dettaglio_text = response.xpath('//*[@class="dettaglio_asta"]//*[@class="dettaglio_text"]')
        for dettaglio in dettaglio_text:
            title = dettaglio.xpath('.//h3/text()').get().strip().replace('\n','')
            
            if "Descrizione" in title:
                product['descrizione'] = "".join(dettaglio.xpath('.//p/text()').getall()).strip().replace('\n','')
            #elif "Dati del lotto" in title:
            elif "Dati del lotto" in title:
                product[title] = {}
                row = dettaglio.xpath('.//*[@class="row"]/div')
                for r in row:
                    spans = r.xpath('.//span')
                    if len(spans) >1:
                        if spans[0].xpath('.//text()').get():
                            key = spans[0].xpath('.//text()').get().strip().replace('\n','').lower().replace(' ','_')
                            value = "".join(spans[1:len(spans)].xpath('.//text()').getall()).strip().replace('\n','')
                            # if key == ""
                            product[title][key] = value
                        else:
                            pass
            else:
                product[title] = {}
                row = dettaglio.xpath('.//*[@class="row"]/div')
                for r in row:
                    spans = r.xpath('.//span')
                    print(len(spans))
                    if len(spans) >1:
                        if spans[0].xpath('.//text()').get():
                            key = spans[0].xpath('.//text()').get().strip().replace('\n','').lower().replace(' ','_')
                            print("key",key)
                            value = ""
                            for s in spans[1:len(spans)]:
                                print('spans elements for value')
                                helper_value =  "".join(s.xpath('.//text()').getall()).strip().replace('\n','')
                                if helper_value not in value and helper_value:
                                    value = value + " " + helper_value
                                    value.strip().replace('\n','')
                            # print(len(spans))
                            # value = " ".join(spans[1:len(spans)].xpath('.//text()').getall()).strip()
                            # print("value",value)
                            # if key == ""
                            print("value",value)
                            product[title][key] = value
                        else:
                            pass
                    
            

                

           
        images = extract_image_urls(response.text)
        product['images'] = images
        files = extract_file_urls(response.text)
        product['files'] = files
        #//*[@data-pn-soggetto-email="val"]
        emails = response.xpath('//*[@data-pn-soggetto-email="val"]/@href').getall()
        emails = [email.replace('mailto:','') for email in emails]
        count = 1
        for email in emails:
            product[f'email{count}'] = email
            count += 1 
        yield product
