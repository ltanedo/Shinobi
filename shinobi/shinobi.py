from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from seleniumwire import webdriver  # Import from seleniumwire
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from seleniumwire.utils import decode
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import json, time

import json
import time
import re
import os

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--no-sandbox')
CHROME_OPTIONS.add_argument('--single-process')
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')
CHROME_OPTIONS.set_capability("goog:loggingPrefs", {"performance": 'ALL'})

DRIVER_PATH = None # f'{os.getcwd()}//chromedriver.exe'
DRIVER      = webdriver.Chrome(options=CHROME_OPTIONS) # webdriver.Chrome(options=chrome_options)

def init(driver=None, chrome_options=None):
    
    if driver:
        global DRIVER
        DRIVER = driver

def fast(url, driver=None):

    init(driver)

    start = time.time()

    DRIVER.get(url)

    return [json.loads(log["message"])["message"] for log in DRIVER.get_log("performance")]

def slow(url, target, driver = None):
    
    if not driver:
        firefoxOptions = FirefoxOptions()
        firefoxOptions.add_argument(argument='--headless')
        driver = webdriver.Firefox(options=firefoxOptions)

    start = time.time()
    driver.get(url)

    collection = []
    for request in driver.requests: 
        if request.response and target in request.url:

            body = ""
            try: 
                body = json.loads(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')))
            except:
                body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))

            collection.append(
                {
                    "request": {
                        'url': request.url,
                        'params': request.params,
                        'headers': {key: value for key, value in (line.split(': ', 1) for line in request.response.headers.as_string().split('\n') if line)}  
                    },
                    "response": body
                }
            )

    print(time.time()-start)
    return collection



