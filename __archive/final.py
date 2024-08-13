from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json
import time

# chromedriver_path = f'{os.getcwd()}//chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-single-click-autofill")
# chrome_options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_experimental_option("prefs", prefs)
# capabilities = DesiredCapabilities.CHROME
# capabilities['goog:loggingPrefs'] = {"performance": 'ALL'}
chrome_options.set_capability("goog:loggingPrefs", {"performance": 'ALL'})


start = time.time()
driver_obj = webdriver.Chrome(options=chrome_options)
driver_obj.get('https://www.nasdaq.com/market-activity/stocks')

# target = "https://api.nasdaq.com"

logs = [json.loads(log["message"])["message"] for log in driver_obj.get_log("performance")]
# logs = [ 
#     record["params"]["request"]
#  for record in logs if "request" in record["params"].keys() and target in record["params"]["request"]["url"]]
time.sleep(10)
print(time.time() - start)
open("z.json",'w').write(json.dumps(logs,indent=2))