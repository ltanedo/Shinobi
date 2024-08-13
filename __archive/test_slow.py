from seleniumwire import webdriver  # Import from seleniumwire
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from seleniumwire.utils import decode
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import json, time
# import asyncio

# Create a new instance of the Chrome driver

# # options = {
# #     'disable_capture': True  # Don't intercept/store any requests
# # }
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46")
# driver = webdriver.Chrome(
#     chrome_options=chrome_options,
#     # seleniumwire_options=options
# )


firefoxOptions = FirefoxOptions()
firefoxOptions.add_argument(argument='--headless')
driver = webdriver.Firefox(options=firefoxOptions)

def slow(url, target):
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

data = slow(
    target = 'api.nasdaq.com',
    url = 'https://www.nasdaq.com/market-activity/stocks'
)

open(f"z.json","w").write(json.dumps(data, indent=2))
