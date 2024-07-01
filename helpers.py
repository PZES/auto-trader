from time import sleep
import random
import requests
from data import accounts
from datetime import datetime
import sqlite3


def fastSleep():
    sleepTime = random.randint(100, 150)
    sleepTime = float(sleepTime / 100)
    sleep(sleepTime)


def slowSleep():
    sleepTime = random.randint(200, 500)
    sleepTime = float(sleepTime / 100)
    sleep(sleepTime)


# Powered By Traider
# https://tradier.com
def getPrice(ticker):
    response = requests.get(
        "https://api.tradier.com/v1/markets/quotes",
        params={"symbols": "{}".format(ticker), "greeks": "false"},
        headers={
            "Authorization": "Bearer {}".format(accounts["Tradier"][0]),
            "Accept": "application/json",
        },
    )
    jsonResponse = response.json()
    bid = float(f"{float(jsonResponse.get('quotes').get('quote').get('bid')):.2f}")
    ask = float(f"{float(jsonResponse.get('quotes').get('quote').get('ask')):.2f}")

    # Don't buy at ask if stock price is messed up
    if bid / ask > 0.80:
        # Buy/sell at market price
        return [ask, bid]
    else:
        with open("data.log", "a") as f:  # Open file in append mode ("a")
            print("Bid ask spread >20%", ticker, file=f)
        # TODO: Ask user for input
        return


# Changes the tickers from a user input string to a 2D array
def setTickers(inputString):
    bs = None
    inputLines = inputString.split("\n")
    tickers = []
    for line in inputLines:
        if line == "":
            continue
        # Buying or selling
        if line in ["b", "s"]:
            bs = line == "b"
            continue
        if bs is None:
            return
        lineParts = line.split(",")
        # Ticker or ticker,quantity
        lineParts.append(bs)
        # Ticker,True/False or ticker,quantity,True/False

        # If quantity not set, set it to 1
        if len(lineParts) == 2:
            lineParts.insert(1, 1)
        # Ticker,quantity,True/False
        price = getPrice(lineParts[0])[0] if bs else getPrice(lineParts[0])[1]
        price = price + (price * 0.06)
        price = round(price, 2)
        lineParts = lineParts[:1] + [price] + lineParts[1:]
        # Ticker,price,quantity,True/False
        tickers.append(lineParts)

    return tickers


def loginLog(platform):
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print("Unable to login to", platform, file=f)


def errorLog(ticker, platform):
    with open("data.log", "a") as f:  # Open file in append mode ("a")
        print(
            "Unable to",
            "buy" if ticker[3] else "sell",
            ticker[0],
            "on",
            platform,
            file=f,
        )


def goodDb(tickerList, platform):
    # Establish database connection and cursor
    conn = sqlite3.connect("tradingLog.db")
    cursor = conn.cursor()

    # Create the log table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        ticker TEXT,
        platform TEXT,
        buy_date TEXT,
        buy_price REAL,
        sell_date TEXT,
        sell_price REAL,
        profit REAL
    )
    """
    )
    conn.commit()

    # Extract ticker details from the list
    bs = tickerList[3]
    price = tickerList[1]
    ticker = tickerList[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if bs:  # If 'buy'
        cursor.execute(
            """
        INSERT INTO log (action, ticker, platform, buy_date, buy_price)
        VALUES (?, ?, ?, ?, ?)
        """,
            ("buy", ticker, platform, now, price),
        )
    else:  # If 'sell'
        # Check if a previous sell operation exists for the same ticker and platform
        cursor.execute(
            """
        SELECT id FROM log
        WHERE action = 'sell' AND ticker = ? AND platform = ?
        """,
            (ticker, platform),
        )

        sellRecord = cursor.fetchone()
        if sellRecord:
            print(
                f"A sell operation for {ticker} on {platform} has already been performed."
            )
        else:
            # Proceed with sell operation
            cursor.execute(
                """
            SELECT id, buy_price, buy_date FROM log
            WHERE action = 'buy' AND ticker = ? AND platform = ?
            ORDER BY id DESC
            LIMIT 1
            """,
                (ticker, platform),
            )

            buyRecord = cursor.fetchone()
            if buyRecord:
                buyId = buyRecord[0]
                buyPrice = buyRecord[1]
                buyDate = buyRecord[2]
                profit = price - buyPrice
                cursor.execute(
                    """
                UPDATE log
                SET action = 'sell', sell_date = ?, sell_price = ?, profit = ?
                WHERE id = ?
                """,
                    (now, price, profit, buyId),
                )
            else:
                print(f"No buy operation found for {ticker} on {platform}.")

    # Commit the changes to the database and close the connection
    conn.commit()
    cursor.close()
    conn.close()
