from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, json, re, requests

def login(account):
    '''
    input  { "email": "deguillacc@yahoo.com", "password": "ChrisThrows90!" }
    success{ "status": 200, "success": true, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNiMzNhYjA1ZTUxYmE5YmJiZTU3ODE4MjM3MjFhMDNlZTI5ZmY5OWRmMzhmY2YxOGRiYjJmNjcwMDE3MDI1OTVlMzUyYWE0OTRjYzk5NjYwIn0.eyJhdWQiOiIxIiwianRpIjoiY2IzM2FiMDVlNTFiYTliYmJlNTc4MTgyMzcyMWEwM2VlMjlmZjk5ZGYzOGZjZjE4ZGJiMmY2NzAwMTcwMjU5NWUzNTJhYTQ5NGNjOTk2NjAiLCJpYXQiOjE3MjI5MTA4NzksIm5iZiI6MTcyMjkxMDg3OSwiZXhwIjoxNzU0NDQ2ODc5LCJzdWIiOiI5ODg4MSIsInNjb3BlcyI6W119.nmSXehG_RYjSKvs9cAuH_z2fulYuUK98KTQotw-MDkw_FpMSVHPzCB1A9liAbh-oXhCdvFyCq0JF5QIgt5dG9dETMwKReBnCMMV7KL_3A3xlvqBeD9k96MjKiPShhCxESluMsuAbG6Rsv8H0fsZmkW_xdlrTqNLOJSQaMDo3sDSlY-TAtvNcItCp7tCl25abCfQzV1I4PUdhRJfcML-mXF6Q0C-KX303AsPNu2wETyLdTnI6w2j0rXajmn6SZqd4t70q_DT5gbREjT-6MazVVfSUHM_CIfGRmc2UxLmtIJaNvEQZpPajUU2pBSluweWW2c9OikuhcXW49mlh-odB0fAUJ6bYXJk63lqq9pQb1zKeOxvVG1Mpbz1C3yCPix2wOiDzVp1KnPGRNyZaJc13YjjyWbn_K68GCYVBIbKCqSPgZ44i18LNqdSHaj7u6MvAByvAU72ZWJlgSsHhZnIQ7I90RxxuMJiyppvTBev_sruNsWS4FKSWICMUxHatZEAmkxllBWVO9mtcTZLFe5la_pOQsVDgbFknCOjpfsEKhy5ZmzBjAa9xJ75leUOVHMlzx9xNwRAcHeb9bAM9L_HYcg6JDesUWVddQYV_ThYLwWgS5b7pnaTD9xFcd7TsgbTtvzxp2jFOq9PhkzRyAU2lf0_V9dfnN5fCexnAxMMzP8Y"}
    fail   {'status':  400, 'success': False, 'message': 'Incorrect credentials'}
    '''
    r = requests.post('https://traq.drivelinebaseball.com/mobile/v1/auth/login',
        json=account,
        verify=False
    )
    return r.json()

def lambda_handler(event, context):
    try:
        # print(json.dumps(event))
        options = Options()
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability("goog:loggingPrefs", {"performance": 'ALL'})
       
    
        driver = webdriver.Chrome(
            service=Service('/opt/chromedriver'),
            options=options
            )
        start = time.time()
        # Go to the Google home page
        driver.get('https://traq.drivelinebaseball.com/login')
        
        # account = {
        #             "email" : "deguillacc@yahoo.com",
        #             "password" : "ChrisThrows90!"
        #         }
        account = {
            "email": event['queryStringParameters']['email'],
            "password": event['queryStringParameters']['password']
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
        pattern = r'remember_web_[a-f0-9]+=[a-zA-Z0-9%_\-\/+=.]+;'
        
        # Search for matches
        
        cookie = re.search(pattern, str(logs))
        cookie = cookie.group()
        user_id = re.search(r"https://traq.drivelinebaseball.com/athlete_dashboard/get-panel/[0-9]+", str(logs))
        user_id = user_id.group().replace("https://traq.drivelinebaseball.com/athlete_dashboard/get-panel/","")
        

        driver.close()
        driver.quit()
    
        token = login(account)['token']
    
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "email": event['queryStringParameters']['email'],
                "user_id": user_id,
                "cookie": cookie,
                "token": token
            })
        }
    except:
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Invalid Credentials!"
            })
        }       

    return response