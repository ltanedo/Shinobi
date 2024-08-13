# Shinobi.py
A fast library to intercept XHR web requests in Python!

# Basics
Shinobi uses selenium and selenium wire to intercept web requests using various techniques depending on the desired speed.

1. Install Requirements
   ```
   pip install requests
   pip install selenium
   pip install selenium wire
   ```
3. import library
   ```
   import shinobi
   ```
5. Slow() function
   > Uses Selenium-Wire to loop and clean all requests
   ```
   shinobi.slow(url="https://www.nasdaq.com/market-activity/stocks")
   ```
   ```
   '''
   [
    {
      "request": {
        "url": "https://api.nasdaq.com/api/marketmovers?assetclass=stocks&exchangeStatus=currentMarket&limit=5",
        "params": {
          "assetclass": "stocks",
          "exchangeStatus": "currentMarket",
          "limit": "5"
        },
        "headers": {
          "content-type": "application/json; charset=utf-8",
          "server": "Kestrel",
        .
        .
        .
   '''
   ```
   
7. Slow() function
   > Dumps in-browser logs very quickly 30x
   ```
   shinobi.fast(url="https://www.nasdaq.com/market-activity/stocks")
   ```
   ```
   '''
   [
      {
        "headers": {
          "Accept": "application/json, text/plain, */*",
          "Referer": "https://www.nasdaq.com/",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
          "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\""
        },
        "initialPriority": "High",
        "isSameSite": true,
        "method": "GET",
        "mixedContentType": "none",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "url": "https://api.nasdaq.com/api/market-info"
      },
      .
      .
      .
   '''
   ```
9. Future Plans
    - Support for new use-cases such as cookie and token searching using regex
    - Increased speed on slow() function
    - Support for target urls



