import redis
from redis import from_url


from seleniumbase import Driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys  # Import the missing module
from selenium.webdriver.support import expected_conditions as EC  # Import the missing module
from selenium.webdriver.common.by import By  # Import the missing module
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import json 
from json.decoder import JSONDecodeError
import random
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
print("proxy:",proxy)

redisClient = redis.from_url('redis://127.0.0.1:6379')
driver = Driver(uc=True,uc_cdp_events=True,headed=True,headless2=True ,no_sandbox=True,proxy=proxy)
driver.maximize_window()

all_urls = []
all_data = []
ids_requests = []   
def push_links_to_redis():
    total = 0 
    for page in range(1, 200):

        
        driver.get(f"https://astegiudiziarie.it/Results?idCategorie={page}")
        print(f'get data from url : https://astegiudiziarie.it/Results?idCategorie={page}')
      
        try:

            for i in range(5000):
                driver.add_cdp_listener("*", lambda data: all_data.append(data))
            listings = WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@class="listing-item"]//h4//a'))
                )
            
            
            html = WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.TAG_NAME, "html"))
                                        )
            
            cond_stop = 0
            while True:
                try:
                    #for a in range(100):
                    html = WebDriverWait(driver, 10).until(
                                        EC.presence_of_all_elements_located((By.XPATH, '//*[@class="listing-item"]'))
                                    )
                    # if cond_stop == 0:
                    #     html[len(html)-1].click()


                    print(f"\033[0;35m\U0001F6A7 Job \033[1;32m Scrolling to download products \033")
                    actions = ActionChains(driver)
                    actions.move_to_element(html[len(html)-1]).send_keys(Keys.PAGE_DOWN).perform()
                    #html[len(html)-1].send_keys(Keys.PAGE_DOWN)
                    
                    for icou in range(6000):
                        driver.add_cdp_listener("*", lambda data: all_data.append(data))
                        #//*[@class="listing-content"]
                    listings = WebDriverWait(driver, 60).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//*[@class="listing-item"]//h4//a'))
                    )
                            
                    results_numbers = WebDriverWait(driver, 100).until(
                                                EC.presence_of_all_elements_located((By.XPATH, '//*[@class="results_number"]'))
                                            )
                                    
                    for r in results_numbers:
                        try :             
                            results_number = int(r.text)
                            
                            break
                        except :
                            pass
                        
                    print("numbers of results:",results_number)
                    total = total + results_number
                    
                    print('listings', len(listings))
                    count = 1
                    all_data_json = []
                    for event in all_data:
                            try:
                                if event["params"]["requestId"] not in ids_requests:
                                    ids_requests.append(event["params"]["requestId"])

                                    try:
                                
                                        d = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': event["params"]["requestId"]})
                                        data_json = json.loads(d['body']) 
                                        #print(data_json)
                                    
                                        for d in data_json:
                                        #all_data_json.extend(data_json)
                                            try:
                                                d['urlSchedaDettagliata'] = "https://astegiudiziarie.it"+d['urlSchedaDettagliata']
                                                all_data_json.append(d)
                                                redisClient.lpush('data_queue:data', json.dumps(d))
                                            except KeyError:
                                                print("no data")
                                    except JSONDecodeError:
                                        pass

                                        
                                    #
                            except Exception as e:
                                print(e)
                                pass
                    print('all_data_json', len(all_data_json))
                    # if len(all_data_json) == 0 :
                    #     driver.refresh()
                    #     cond_stop += 1

                    if len(listings) == results_number :
                        cond_stop = 0
                        # for icou in range(100):
                        #     driver.add_cdp_listener("*", lambda data: all_data.append(data))
                        break
                except UnexpectedAlertPresentException:
                    pass

        except :

            pass
         





if __name__ == '__main__':
    push_links_to_redis()
    
   

