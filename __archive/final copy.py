from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json
import time
import re

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
driver = webdriver.Chrome(options=chrome_options)
# Go to the Google home page
driver.get('https://traq.drivelinebaseball.com/login')

account = {
            "email" : "deguillacc@yahoo.com",
            "password" : "ChrisThrows90!"
        }

# Find the input element
input_element = driver.find_element("id", "email")
input_element.send_keys(account['email'])
input_element = driver.find_element("id", "password")
input_element.send_keys(account['password'])
# Find the button element
button_element = driver.find_element("css selector", "button[type='submit']")
button_element.click()


driver.get('https://traq.drivelinebaseball.com/profile/tab-1')

target = "traq.drivelinebaseball"

logs = [json.loads(log["message"])["message"] for log in driver.get_log("performance")]
logs = [ 
    record["params"] #["request"]
        for record in logs 
                # if "request" in record["params"].keys() 
                # and target in str(record["params"]["request"])
                # if "request" in record["params"].keys() 
                #     and "url" in record["params"]["request"]
                #         and target in record["params"]["request"]["url"] 
]


match = re.search(r'remember_web_[a-f0-9]+', str(logs))
match = match.group()
id = re.search(r"https://traq.drivelinebaseball.com/athlete_dashboard/get-panel/[0-9]+", str(logs))
id = id.group().replace("https://traq.drivelinebaseball.com/athlete_dashboard/get-panel/","")
print(id)
# "https://traq.drivelinebaseball.com/athlete_dashboard/get-panel/98881"
quit()

print(json.dumps(logs,indent=2))
print(time.time() - start)
open("z2.json",'w').write(json.dumps(logs,indent=2))


# driver.get('https://traq.drivelinebaseball.com/profile/tab-1')

# target = "https://api.nasdaq.com"

# logs = [json.loads(log["message"])["message"] for log in driver.get_log("performance")]
# logs = [ 
#     record["params"]["request"]
#  for record in logs if "request" in record["params"].keys() and target in record["params"]["request"]["url"]]

# print(time.time() - start)
# open("z.json",'w').write(json.dumps(logs,indent=2))