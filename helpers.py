from time import sleep
import random
import requests
from data import accounts

def fastSleep():
    time = random.randint(100,150)
    time = float(time/100)
    sleep(time)

def slowSleep():
    time = random.randint(200,500)
    time = float(time/100)
    sleep(time)

#Powered By Traider
#https://tradier.com
def getPrice(ticker):
    response = requests.get('https://api.tradier.com/v1/markets/quotes',
        params={
            'symbols': '{}'.format(ticker), 
            'greeks': 'false'},
        headers={
            'Authorization': 'Bearer {}'.format(accounts['Tradier'][0]), 
            'Accept': 'application/json'}
    )
    json_response = response.json()
    bid = float(f"{float(json_response.get('quotes').get('quote').get('bid')):.2f}")
    ask = float(f"{float(json_response.get('quotes').get('quote').get('ask')):.2f}")

    #dont buy at ask if stock price is messed up
    if(bid/ask > .90):
        #buy/sell at market price
        
        return [ask,bid]
    else:
        return[bid,ask]

#changes the tickers from a user input string to a 2d array
def setTickers(input):
    bs = None
    input = input.split('\n')
    tickers = []
    for i in range(len(input)):
        if input[i] == '':
            continue
        #buying or selling
        if input[i] in ['b','s']:
            bs = (input[i] == 'b')
            continue
        if bs is None:
            return
        input[i] = input[i].split(",")
        #ticker or ticker,quant
        input[i].append(bs)
        #ticker,T/F or ticker,quant,T/F

        #if quantity not set, set it to 1
        if(len(input[i]) == 2):
            input[i].insert(1, 1)
        #ticker,quant,T/F
        price = getPrice(input[i][0])[0] if bs else getPrice(input[i][0])[1]
        input[i] = input[i][:1]+[price]+input[i][1:]
        #ticker,price,quant,T/F
        tickers.append(input[i])

    return(tickers)

def loginLog():
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print()
def errorLog(ticker, bs, platform):
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        (print('unable to','buy' if bs else 'sell', ticker, 'on', platform,  file=f))
