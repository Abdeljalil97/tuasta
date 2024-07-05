from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import asyncio
from seleniumbase import Driver
import random
import redis
from sbvirtualdisplay import Display
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys  # Import the missing module
from selenium.webdriver.support import expected_conditions as EC  # Import the missing module
from selenium.webdriver.common.by import By  # Import the missing module
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase import SB
display = Display(visible=0, size=(1440, 1880))
display.start()
proxies = ["14a6fd93550c9:44c5fce127@185.87.77.25:12323",
           "14a6fd93550c9:44c5fce127@92.61.108.70:12323",
           "14a6fd93550c9:44c5fce127@194.180.27.32:12323",
           "14a6fd93550c9:44c5fce127@217.67.77.181:12323",
           "14a6fd93550c9:44c5fce127@176.124.75.223:12323",]
proxy = random.choice(proxies)
driver_helper = Driver(uc=True,no_sandbox=True, proxy=proxy,headed=True,uc_cdp_events=True,headless2=True)



redisClient = redis.from_url('redis://127.0.0.1:6379')


def get_all_links():
    
    #proxies = ["14a6fd93550c9:44c5fce127@185.87.77.25:12323",
       #    "14a6fd93550c9:44c5fce127@92.61.108.70:12323",
      #     "14a6fd93550c9:44c5fce127@194.180.27.32:12323",
      #     "14a6fd93550c9:44c5fce127@217.67.77.181:12323",
     #      "14a6fd93550c9:44c5fce127@176.124.75.223:12323",]
    #proxy = random.choice(proxies)
    print("proxy:",proxy)
    urls = ["https://www.astalegale.net/Mobili?limit=120&mode=grid&page=1","https://www.astalegale.net/Immobili?limit=120&mode=grid&page=1"]

    #driver_helper = Driver(uc=True,uc_cdp_events=True,proxy=proxy)
    for url in urls:
    #driver_helper =  Driver(undetectable=True, uc_cdp_events=True,chromium_arg="log-level=3,disable-logging",proxy=)

        driver_helper.get(url)
        driver_helper.maximize_window()
        driver_helper.sleep(5)
        try:
            pass_alert = WebDriverWait(driver_helper, 30).until(
                                            EC.presence_of_element_located((By.XPATH, '//*[@class="iubenda-cs-cwa-button"]'))
                                        )
            pass_alert.click()
        except TimeoutException:
            pass
    #//*[@class="page-item"]/button
        pages = WebDriverWait(driver_helper, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="page-item"]/button')))
        pages = [page.text for page in pages]
        end_page = pages[-2]
        print("end_page:",pages)
        end_page = int(end_page.strip())

        for page in range(1,end_page+1):
            driver_helper.get(url.replace("page=1",f"page={page}"))
            
            
        #//*[@class="result-content"]//*[@class="grid"]//*[@class="card-header"]//a
            links = WebDriverWait(driver_helper, 30).until(
                                            EC.presence_of_all_elements_located((By.XPATH, '//*[@class="result-content"]//*[@class="grid"]//*[@class="card-header"]//a'))
                                        )
            links = [link.get_attribute('href') for link in links]
            for link in links:
                redisClient.lpush('data_queue:astalegale',link)


     
            
           
    #return all_links   

get_all_links()
