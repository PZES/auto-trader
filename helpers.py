from time import sleep
import random
import requests
from data import accounts
import sqlite3

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
    if(bid/ask > .80):
        #buy/sell at market price
        return [ask,bid]
    else:
        with open("data.log", "a") as f:  # Open file in append mode ("a")
            print('bid ask spread >20%', ticker, file=f)
        #TODO ask user for input
        return

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

def loginLog(platform):
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print('unabele to login to', platform, file=f)

def errorLog(ticker, platform):
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print('unable to','buy' if ticker[3] else 'sell', ticker[0], 'on', platform,  file=f)

def goodDB(bs, ticker, platform, price):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if bs:  # If 'buy'
        cursor.execute('''
        INSERT INTO log (action, ticker, platform, buy_date)
        VALUES (?, ?, ?, ?)
        ''', ('buy', ticker, platform, now))
    else:  # If 'sell'
        # Check if a previous sell operation exists for the same ticker and platform
        cursor.execute('''
        SELECT id FROM log
        WHERE action = 'sell' AND ticker = ? AND platform = ?
        ''', (ticker, platform))
        
        sellRecord = cursor.fetchone()
        if sellRecord:
            print(f"A sell operation for {ticker} on {platform} has already been performed.")
        else:
            # Proceed with sell operation
            cursor.execute('''
            SELECT id, buy_date FROM log
            WHERE action = 'buy' AND ticker = ? AND platform = ?
            ORDER BY id DESC
            LIMIT 1
            ''', (ticker, platform))
            
            buyRecord = cursor.fetchone()
            if buyRecord:
                buyId = buyRecord[0]
                buyDate = buyRecord[1]
                profit = price - cursor.execute('SELECT sell_price FROM log WHERE id=?', (buyId,)).fetchone()[0]
                cursor.execute('''
                UPDATE log
                SET action = 'sell', sell_date = ?, sell_price = ?, profit = ?
                WHERE id = ?
                ''', (now, price, profit, buyId))
            else:
                print(f"No buy operation found for {ticker} on {platform}.")
    
    # Commit the changes to the database
    conn.commit()
