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

    #just checking if the bid ask is really messed up
    if(bid/ask > .90):
        #buy/sell at market price
        
        return [ask,bid]
    else:
        return[bid,ask]

#changes the tickers from a user input string to a 2d array
def setTickers(tickers):
    bs = None
    tickers = tickers.split('\n')
    for i in range(len(tickers)):
        if tickers[i] == '':
            continue
        #buying or selling
        if tickers[i] in ['b','s']:
            bs = (tickers[i] == 'b')
            continue
        if bs is None:
            return
        tickers[i] = tickers[i].split(",")
        #ticker or ticker,quant
        tickers[i].append(bs)
        #ticker,T/F or ticker,quant,T/F

        #if quantity not set, set it to 1
        if(len(tickers[i]) == 2):
            tickers[i].insert(1, 1)
        #ticker,quant,T/F
        price = getPrice(tickers[i][0])[0] if bs else getPrice(tickers[i][0])[1]
        tickers[i] = tickers[i][:1]+[price]+tickers[i][1:]
        #ticker,price,quant,T/F

    return(tickers)

def errorLog():
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print("Executing with accounts:", accounts, file=f)
        print("Executing with tickers:", tickers, file=f)
        print("Execution successful", file=f)