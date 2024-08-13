import shinobi

data = shinobi.slow(
    target = 'api.nasdaq.com',
    url = 'https://www.nasdaq.com/market-activity/stocks'
)
print(data)

data = shinobi.fast("https://www.nasdaq.com/market-activity/stocks/aapl")
print(data)