"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from .http import SeleniumbaseRequest
import random
import time
from sbvirtualdisplay import Display
import random
display = Display(visible=0, size=(1440, 1880))
display.start()
class SeleniumbaseMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, driver_name, driver_executable_path, driver_arguments,
        browser_executable_path):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }
        
        self.driver = None
       
       
       

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        # if not driver_name or not driver_executable_path:
        #     raise NotConfigured(
        #         'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
        #     )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumbaseRequest):
            return None
        #self.driver = Driver(uc=True)
        number_of_retries = 0
        if str(request.url).startswith("https://astegiudiziarie.it/"):
            while True:
                
                proxies = ["14a6fd93550c9:44c5fce127@185.87.77.25:12323",
                        "14a6fd93550c9:44c5fce127@92.61.108.70:12323",
                        "14a6fd93550c9:44c5fce127@194.180.27.32:12323",
                        "14a6fd93550c9:44c5fce127@217.67.77.181:12323",
                        "14a6fd93550c9:44c5fce127@176.124.75.223:12323",]
                proxy = random.choice(proxies)
                print("proxy:",proxy)
                self.driver = Driver(uc=True,no_sandbox=True,incognito=True, proxy=proxy,headed=True,uc_cdp_events=True,headless2=True)
                self.driver.get(request.url)
                self.driver.maximize_window()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                #//*[@class="title-bar-auction-left"]
                try:
                    number_of_retries += 1
                    print(f"try {number_of_retries}")
                    numero = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="title-bar-auction-left"]'))
                    )
                    
                    print("numero",numero.text)

                    
                        

                    break
                except Exception as e:
                    print("error",e)
                    if number_of_retries == 10:
                        print("retrying 10 times")
                        break
                    print(f"retrying ...with {request.url}")
                    self.driver.quit()

                    
            for cookie_name, cookie_value in request.cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            if request.wait_until:
                WebDriverWait(self.driver, request.wait_time).until(
                    request.wait_until
                )

            if request.screenshot:
                request.meta['screenshot'] = self.driver.get_screenshot_as_png()

            if request.script:
                self.driver.execute_script(request.script)

            body = str.encode(self.driver.page_source)

            # Expose the driver via the "meta" attribute
            request.meta.update({'driver': self.driver})

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
        else:
            print(f"wrong link: {request.url}")
            pass
        

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()

