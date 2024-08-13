from seleniumwire import webdriver  # Import from seleniumwire
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from seleniumwire.utils import decode
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import json, time
import asyncio

# Create a new instance of the Chrome driver

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46")

options = {
    'disable_capture': True  # Don't intercept/store any requests
}

firefoxOptions = FirefoxOptions()
firefoxOptions.add_argument(argument='--headless')
start = time.time()
# driver = webdriver.Chrome(
#     chrome_options=chrome_options,
#     seleniumwire_options=options
# )

driver = webdriver.Firefox(options=firefoxOptions)


async def one():


    options = {
        'disable_capture': False,  # Don't intercept/store any requests
        'disable_encoding': False
    }

    driver.get('https://www.nasdaq.com/market-activity/stocks')

    target = 'api.nasdaq.com'
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

    open("stocks.json","w").write(json.dumps(collection, indent=2))

    print(time.time()-start)

async def two():

    options = {
        'disable_capture': False,  # Don't intercept/store any requests
        'disable_encoding': False
    }
    driver.get('https://www.nasdaq.com/market-activity/stocks/tsla')

    target = 'api.nasdaq.com'
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

    open("tsla.json","w").write(json.dumps(collection, indent=2))

    print(time.time()-start)


async def main():
    # tasks = [
    #     asyncio.to_thread(one),
    #     asyncio.to_thread(two)
    # ]

    await one()
    await two()
        
    # await asyncio.gather(*tasks)

    print("finished")

if __name__ ==  '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())