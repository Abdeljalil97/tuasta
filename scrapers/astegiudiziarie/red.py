from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys  # Import the missing module
from selenium.webdriver.support import expected_conditions as EC  # Import the missing module
from selenium.webdriver.common.by import By  # Import the missing module
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import json
from json.decoder import JSONDecodeError
import random
#from seleniumwire.utils import decode , decoder
from sbvirtualdisplay import Display
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys  # Import the missing module
from selenium.webdriver.support import expected_conditions as EC  # Import the missing module
from selenium.webdriver.common.by import By  # Import the missing module
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase import SB
import time
import redis
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

#import undetected_chromedriver as uc
from sbvirtualdisplay import Display
import random
display = Display(visible=0, size=(1440, 1880))
display.start()


redisClient = redis.from_url('redis://127.0.0.1:6379')

proxies = ["14a6fd93550c9:44c5fce127@185.87.77.25:12323",
        "14a6fd93550c9:44c5fce127@92.61.108.70:12323",
        "14a6fd93550c9:44c5fce127@194.180.27.32:12323",
        "14a6fd93550c9:44c5fce127@217.67.77.181:12323",
        "14a6fd93550c9:44c5fce127@176.124.75.223:12323",]
proxy = random.choice(proxies)
# Set up Chrome options
print(proxy)
# options = uc.ChromeOptions()
# #options.add_argument("--auto-open-devtools-for-tabs")
# options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
# Initialize the WebDriver
#driver = uc.Chrome(options=options)
print('open the browser')
driver = Driver(uc=True,incognito=True,proxy=proxy)
# Enable Network logging
print("open the browser")
driver.execute_cdp_cmd('Network.enable', {})

# URL to navigate to
urls = [
    "https://astegiudiziarie.it/Immateriali/Risultati",
    # "https://astegiudiziarie.it/Aziende/Risultati",
    # "https://astegiudiziarie.it/Results"
]
for page in range(1, 200):
    #driver.get(url)
#?idCategorie={page}
    try:
        driver.get(f"https://astegiudiziarie.it/Results?idCategorie={page}")

        while True:
            html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "html"))
            )
            html.click()
            print("Scrolling to download previous messages .....")
            html.send_keys(Keys.PAGE_DOWN)

            results_number = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@class="dettagliRicerca"]//strong'))
            )

            for r in results_number:
                try:
                    results_number = int(r.text)
                    break
                except:
                    pass

            load_results = WebDriverWait(driver, 120).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="boxRisultati"]/div/div//a[1]'))
            )

            print(f"results_number : {results_number} , load_results : {len(load_results)}")

            if results_number == len(load_results):
                break
    except Exception as e:
        print(e)
        pass
#    links = [l.get_attribute('href') for l in load_results]
 #   print(links)
  #  print(len(links))
   # for link in links:
    #    d = {'url':link}
     #   redisClient.lpush('data_queue:data', json.dumps(d))
        #print(request.headers)
    # time.sleep(15)
    # logs = driver.get_log('performance')
    # print(logs)
    # requests_ids = []
    # for event in logs:
    #     if "requestId" in str(event):
    #         request_id = str(event).split('"requestId":')[1].split(',')[0].split('"')[1].strip()
    #         if request_id not in requests_ids:
    #             requests_ids.append(request_id)

    # for id in requests_ids:
    #     try:

    #         d = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': str(id)})
    #         data_json = json.loads(d['body'])
    #         print(len(data_json))
    #         for d in data_json:
    #             print(d['idAsta'])
    #             print(d['urlSchedaDettagliata'])
    #             #all_data_json.extend(data_json)
    #             try:
    #                 d['urlSchedaDettagliata'] = "https://astegiudiziarie.it"+d['urlSchedaDettagliata']
    #                 #all_data_json.append(d)
    #                 redisClient.lpush('data_queue:data', json.dumps(d))
    #                 print("data pushed")

    #             except KeyError:
    #                 print("no data")
    #     except Exception as e :
    #         print(e)
    #         pass
    # for entry in logs:
    #     log = json.loads(entry['message'])['message']
    #     if log['method'] == 'Network.responseReceived':
    #         response = log['params']['response']
    #         if 'video' in response['mimeType'] or 'audio' in response['mimeType']:
    #             print(f"URL: {response['url']}")
    #             print("Response Headers:")
    #             for header, value in response['headers'].items():
    #                 print(f"{header}: {value}")
    #             print("\n")

driver.quit()
