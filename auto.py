
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests,math
Buy = True
Sell = False


#ally ****WORKS**** TODO change limit to be ask instead of bid 
#fidelity ****WORKS**** on all but margin
#firstrade ****WORKS**** TODO change limit to be ask instead of bid
#plynk ****APP ONLY****
#public 1.00 min on website ****WORKS**** TODO add sell
#robinhood  ****WORKS**** TODO add sell
#schwab setup ****WORKS**** TODO add quantity >1 
#sofi ****WORKS TODO setup login and sell
#stocktwits ****WORKS**** TODO add sell
#tastytrade
#tradier API is fire ****WORKS****
#vanguard ****WORKS**** 
#wellsfargo ****WORKS****

#google-chrome-stable --remote-debugging-port=9222
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def schwabLogin():
    #schwab login page
    driver.get("https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx")
    #click login
    iframe = driver.find_element(By.ID, "lmsSecondaryLogin")
    driver.switch_to.frame(iframe)

    #wait for autocomplete
    sleep(10)
    driver.find_element(By.ID, "btnLogin").click()

def schwabExec(accounts, tickers, action, quantity):
    driver.get("https://client.schwab.com/app/trade/tom/#/trade")
    sleep(5)
    #loop through accounts
    for i in range(accounts):
        driver.find_element(By.XPATH, "//sdps-account-selector/div/div/button").click()
        driver.find_element(By.XPATH, "//a[@id='basic-example-small-header-0-account-" + str(i) + "']").click()

        #loop through tickers
        for ticker in tickers:
            sleep(5)
            tickerBox = driver.find_element(By.ID, "_txtSymbol")
            tickerBox.send_keys(ticker)
            tickerBox.send_keys(Keys.ENTER)
            sleep(2)
            #action
            actionBox = Select(driver.find_element(By.ID, "_action"))
            if(action):
                #buy
                actionBox.select_by_visible_text('Buy')   
            else:
                #sell
                actionBox.select_by_visible_text('Sell') 
            
            #quantity
            #TODO

            #review
            driver.find_element(By.CSS_SELECTOR, ".mcaio-order--reviewbtn").click()
            #place
            sleep(2)
            driver.find_element(By.ID, "mtt-place-button").click()
            #place another
            sleep(2)
            driver.find_element(By.CSS_SELECTOR, ".mcaio--mcaio-cta-buttons-anothertrade").click()

#click not working idk
def fidelityLogin():
    #driver.get("https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://digital.fidelity.com/ftgw/digital/portfolio/summary")
    #sleep(10)
    driver.find_element(By.CSS_SELECTOR, ".main-container").click()
    driver.find_element(By.CSS_SELECTOR, ".pvd-button__contents").click()

def fidelityExec(accounts, tickers, action, quantity,price):

    for account in accounts:
        for ticker in tickers:
            if(action):
                act = "B"
            else:
                act = "S"
            driver.get("https://digital.fidelity.com/ftgw/digital/trade-equity/index?ORDER_TYPE=E&ACCOUNT="+account+"&SYMBOL="+ticker+"&PRICE_TYPE=L&ORDER_ACTION="+act+"&QTY="+str(quantity))#
            sleep(5)
            #set limit price
            driver.find_element(By.ID, "eqt-mts-limit-price").send_keys(price)
            sleep(1)

            #preview
            driver.find_element(By.CSS_SELECTOR, "#previewOrderBtn .pvd3-button-root").click()
            sleep(2)
            

            #place
            driver.find_element(By.ID, "placeOrderBtn").click()

#does not click for some reason 
def vanguardLogin():
    driver.get("https://holdings.web.vanguard.com/")
    sleep(10)
    driver.find_element(By.XPATH, "//*[@id='username-password-submit-btn-1']").click()

def vanguardExec(accounts, tickers, action, quantity, price):

    #loop through accounts
    for i in range(accounts):
        for ticker in tickers:
            driver.get("https://personal.vanguard.com/us/buysell/web/tradeticket/TradeTicket.xhtml?investmentType=EQUITY")
            sleep(10)
            #chnage account
            driver.execute_script("const xpath = '/html/body/div[3]/div[5]/span/div/span[3]/div/div[1]/div/div[2]/div/span/span[2]/div/div/div[1]/span/div/p[1]/b'; const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (element && element.textContent === 'Incomplete transaction detected') {    const okButton = document.getElementById('okButtonInput');    if (okButton) {        okButton.click();    } } ")
            driver.find_element(By.ID, "baseForm:accountSelectOne_text").click()
            driver.execute_script("return !(document.querySelector('.vg-SelOneMenuFocusText'));")
            test = driver.find_element(By.ID, "baseForm:accountSelectOne:"+str(i+1)).click()
            #action
            sleep(5)
            driver.find_element(By.ID, "baseForm:transactionTypeSelectOne").click()
            sleep(1)
            if(action):
                driver.find_element(By.ID, "baseForm:transactionTypeSelectOne:1").click()
            else:
                driver.find_element(By.ID, "baseForm:transactionTypeSelectOne:0").click()

            #ticker
            tickerBox = driver.find_element(By.ID, "baseForm:investmentTextField")
            #ticker.click()
            tickerBox.send_keys(ticker)
            #sleep(5)
            #quantity
            driver.find_element(By.ID, "baseForm:shareQuantityTextField").click()
            sleep(1)
            driver.execute_script("input = document.getElementById('baseForm:shareQuantityTextField'); input.select(); input.value='"+str(quantity)+"'; input.setAttribute('value', input.value);")  

            #order type
            driver.find_element(By.ID, "baseForm:orderTypeSelectOne_text").click()
            sleep(1)
            driver.find_element(By.ID, "baseForm:orderTypeSelectOne:2").click()
            sleep(1)

            #limit price
            driver.find_element(By.ID, "baseForm:limitPriceTextField").click()
            sleep(1)
            driver.execute_script("input = document.getElementById('baseForm:limitPriceTextField'); input.select(); input.value='"+str(price)+"'; input.setAttribute('value', input.value);") 

            #duration
            driver.find_element(By.ID, "baseForm:durationTypeSelectOne_text").click()
            sleep(1)
            driver.find_element(By.ID, "baseForm:durationTypeSelectOne:1").click()

            #continue
            driver.find_element(By.ID, "baseForm:reviewButtonInput").click()
            sleep(6)
            #submit
            driver.find_element(By.ID,"baseForm:submitButtonInput").click()
            sleep(1)

def wellsFargoLogin():
    driver.get("https://connect.secure.wellsfargo.com/auth/login/present")
    sleep(10)
    login = driver.find_element(By.CSS_SELECTOR, ".Button__modern___cqCp7")
    login.click()

def wellsFargoExec(accounts, tickers, action, quantity, price):
    #navigate to it cuz wellsfargo got weird links
    driver.find_element(By.XPATH, "//*[@id='BROKERAGE_LINK7P']").click()
    sleep(10)
    driver.find_element(By.XPATH, "//*[@id='trademenu']/span[1]").click()
    sleep(5)
    driver.find_element(By.XPATH, "//*[@id='linktradestocks']").click()

    driver.find_element(By.XPATH, "//*[@id='dropdown2']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//*[@id='dropdownlist2']/li[1]").click()
    sleep(1)

    for i in range(accounts):
        driver.find_element(By.XPATH, "//*[@id='dropdown2']").click()
        sleep(1)
        driver.find_element(By.XPATH, "//*[@id='dropdownlist2']/li["+ str(i+1) +"]").click()
        sleep(1)   
        driver.find_element(By.XPATH, "//*[@id='btn-continue']").click()
    
        for ticker in tickers:
            #action
            actionBox = driver.find_element(By.ID, "BuySellBtn")
            actionBox.click()
            if(action):
                action = driver.find_element(By.LINK_TEXT, "Buy")
                action.click()
            else:
                action = driver.find_element(By.LINK_TEXT, "Sell")
                action.click()
        
            #ticker
            tickerBox = driver.find_element(By.ID, "Symbol")
            tickerBox.send_keys(ticker)
            tickerBox.send_keys(Keys.ENTER)

            sleep(1)
            #quantity
            tickerBox = driver.find_element(By.ID, "OrderQuantity")
            tickerBox.send_keys(quantity)
            tickerBox.send_keys(Keys.ENTER)

            #order type
            orderBox = driver.find_element(By.ID, "OrderTypeBtnText")
            orderBox.click()
            sleep(1)
            order = driver.find_element(By.LINK_TEXT, "Limit")  
            order.click()

            #limit price
            tickerBox = driver.find_element(By.ID, "Price")
            tickerBox.send_keys(price)
            tickerBox.send_keys(Keys.ENTER)

            #timing
            timingBox = driver.find_element(By.ID, "TIFBtn")
            timingBox.click()
            timing = driver.find_element(By.LINK_TEXT, "Day")
            timing.click()

            #preview
            review = driver.find_element(By.ID, "actionbtnContinue")
            review.click()
            sleep(5)
            #submit
            submit = driver.find_element(By.CSS_SELECTOR, ".btn-wfa-submit")
            submit.click()
            sleep(5)
            driver.find_element(By.CSS_SELECTOR, ".btn-wfa-primary").click()

def firstradeLogin():
    #driver.get("https://invest.firstrade.com/cgi-bin/login")
    #sleep(10)
    driver.find_element(By.ID, "loginButton").click()

def firstradeExec(accounts, tickers, action, quantity):
    driver.get("https://invest.firstrade.com/cgi-bin/main#/cgi-bin/stock_order")
    sleep(5)
    for account in accounts:
        Select(driver.find_element(By.ID, "accountId1")).select_by_visible_text(account)
        print(account)
        sleep(2)
        for ticker in tickers:
            if(action):
                driver.find_element(By.ID, "transactionType_Buy1").click()
            else:
                driver.find_element(By.ID, "transactionType_Sell1").click()

            #quantity
            driver.find_element(By.ID, "quantity1").send_keys(quantity)

            #ticker
            driver.find_element(By.ID, "symbol1").send_keys(ticker)

            driver.find_element(By.ID, "limitPrice1").click()
            

            #submit
            sleep(2)
            driver.find_element(By.ID, "submitOrder1").click()

            #place another
            sleep(3)
            driver.find_element(By.CSS_SELECTOR, ".submitted_placeorder_bnt").click()
            sleep(2)

def allyLogin():
    driver.get("https://secure.ally.com/")
    sleep(10)
    driver.find_element(By.XPATH, "//*[contains(@id,'login-button')]").click()

def allyExec(accounts, tickers, action, quantity):
    #driver.get("https://live.invest.ally.com/trading-full/stocks")
    #sleep(6)
    for account in accounts:
        driver.find_element(By.XPATH, "//*[@id='account-details-account-number']/select").click()
        Select(driver.find_element(By.XPATH, "//*[@id='account-details-account-number']/select")).select_by_visible_text(account)
        for ticker in tickers:
            tickerBox = driver.find_element(By.CSS_SELECTOR, ".styled-input")
            tickerBox.click()
            tickerBox.send_keys("F")
            tickerBox.send_keys(Keys.ENTER)
            sleep(3)

            if(action):
                driver.find_element(By.XPATH, "//span[contains(.,'Buy')]").click()
            else:
                driver.find_element(By.XPATH, "//span[contains(.,'Sell')]").click()

            quant = driver.find_element(By.CSS_SELECTOR, ".stepper-input")
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(quantity)

            driver.find_element(By.CSS_SELECTOR, "#stock-limit > span").click()

            limitBox = driver.find_element(By.CSS_SELECTOR, "#stock-limit-input .stepper-input")
            
            sleep(1)
            #preview
            driver.find_element(By.XPATH, "//*[@id='content']/div/div[3]/ally-card/section/div/section-order-summary/div[2]/div/div[1]/ally-button/button").click()
            sleep(3)
            
            #place order
            driver.find_element(By.XPATH, "//*[@id='trade-preview']/div/table/tbody/tr/td[2]/div/button").click()
            sleep(2)

            #okay
            driver.find_element(By.XPATH, "//*[@id='trade-complete']/div[3]/ally-button/button").click()
            sleep(1)

def tradierExec(accounts, tickers, action, quantity, tradierToken):
    for account in accounts:
        for ticker in tickers:
            if(action):
                side = 'buy'
            else:
                side = 'sell'
            headers = {
            'Authorization': 'Bearer {}'.format(tradierToken), 
            'Accept': 'application/json'
            }
            url = 'https://api.tradier.com/v1/accounts/{}/orders'.format(account)
            response = requests.post(url,
            data={'class': 'equity', 'symbol': ticker, 'side': side, 'quantity': quantity, 'type': 'market', 'duration': 'day'},
            headers=headers
            )
            json_response = response.json()

#TODO setup sell
def stocktwitsExec(tickers,action,quantity):
    for ticker in tickers:
        driver.get("https://stocktwits.com/symbol/"+ ticker)
        driver.find_element(By.NAME, "quantity").send_keys(quantity)

        #review
        driver.find_element(By.CSS_SELECTOR, ".Button_lg__pKIqa")

        #complete
        driver.find_element(By.CSS_SELECTOR, ".Button_lg__pKIqa")

#TODO
def sofiLogin():
    return

#TODO setup sell
def sofiExec(accounts, tickers, action, quantity, price):
    for ticker in tickers:
        #driver.get("https://www.sofi.com/wealth/app/stock/"+ticker)
        for account in accounts:
            sleep(10)  
            
            buy = driver.find_element(By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button")
            if not (buy.is_enabled()):
                print("not on SOFI")
                return
            driver.find_element(By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button").click()
            sleep(3)
            Select(driver.find_element(By.XPATH, "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[1]/div/select")).select_by_visible_text(account)
            sleep(2)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/input").send_keys(quantity)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[4]/div[2]/input").send_keys(price)
            driver.find_element(By.CSS_SELECTOR, ".StyledActionButton-hdOdyk").click()
            sleep(3)
            driver.find_element(By.CSS_SELECTOR, ".StyledActionButton-hdOdyk").click()
            sleep(1)
            driver.find_element(By.XPATH, "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/button").click()

#TODO
def robinhoodLogin():
    return

#TODO sell
def robinhoodExec(accounts, tickers, action, quantity):
    for ticker in tickers:
        driver.get("https://robinhood.com/stocks/"+ticker)
        sleep(10)
        for i in range(accounts):
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/main/div/aside/div[1]/form/button").click()
            driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[3]/div/div/button["+str(i+1)+"]").click()

            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/main/div/aside/div[1]/form/div[2]/div/div[2]/div/div/div/div/input").send_keys(quantity)
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/main/div/aside/div[1]/form/div[3]/div/div[2]/div/div/button").click()
            sleep(1)
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/main/div/aside/div[1]/form/div[3]/div/div[2]/div/div/button").click()
            sleep(3)
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/main/div/aside/div[1]/div/div[2]/div/button").click()

#TODO sell
def publicExec(tickers,action,quantity, price):
    for ticker in tickers:
        driver.get("https://public.com/stocks/"+ticker)
        shares = int(math.ceil(1/price))
        sleep(7)
        #click buy 
        driver.find_element(By.XPATH, "//*[@id='maincontent']/div/div[2]/div[1]/div/div/div/button[1]/span").click()
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[1]/div/button").click()
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[1]/div/div/button[2]").click()
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[4]/div[1]/div/div[1]/input").send_keys(shares)
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[5]/button").click()
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[3]/button").click()
        sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[2]/button").click()


