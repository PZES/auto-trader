import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests, math

from helpers import *

Buy = True
Sell = False

options = uc.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = uc.Chrome(options=options)
# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def allyLogin():
    try:
        driver.get("https://secure.ally.com/")
        slowSleep()
        driver.find_element(By.XPATH, "//*[contains(@id,'login-button')]").click()
    except:
        loginLog("Ally")


def allyExec(accounts, tickers):
    # driver.get("https://live.invest.ally.com/trading-full/stocks") #TODO the popup messes thie up
    slowSleep()
    for account in accounts:
        try:
            driver.find_element(
                By.XPATH, "//*[@id='account-details-account-number']/select"
            ).click()
            Select(
                driver.find_element(
                    By.XPATH, "//*[@id='account-details-account-number']/select"
                )
            ).select_by_visible_text(account)
        except:
            print("changing account failed")
        for ticker in tickers:
            # try:
            tickerBox = driver.find_element(By.CSS_SELECTOR, ".styled-input")
            tickerBox.click()
            tickerBox.send_keys(ticker[0])
            tickerBox.send_keys(Keys.ENTER)
            fastSleep()

            if ticker[3]:
                driver.find_element(By.XPATH, "//span[contains(.,'Buy')]").click()
            else:
                driver.find_element(By.XPATH, "//span[contains(.,'Sell')]").click()

            quant = driver.find_element(By.CSS_SELECTOR, ".stepper-input")
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(Keys.BACKSPACE)
            quant.send_keys(ticker[2])

            driver.find_element(By.CSS_SELECTOR, "#stock-limit > span").click()

            limitBox = driver.find_element(
                By.CSS_SELECTOR, "#stock-limit-input .stepper-input"
            )

            fastSleep()
            # preview
            driver.find_element(
                By.XPATH,
                "//*[@id='content']/div/div[3]/ally-card/section/div/section-order-summary/div[2]/div/div[1]/ally-button/button",
            ).click()
            slowSleep()

            # place order
            driver.find_element(
                By.XPATH, "//*[@id='trade-preview']/div/table/tbody/tr/td[2]/div/button"
            ).click()
            slowSleep()

            # okay
            driver.find_element(
                By.XPATH, "//*[@id='trade-complete']/div[3]/ally-button/button"
            ).click()
            fastSleep()
            goodDB(ticker, account + " in Ally")
            # except:
            # errorLog(ticker,account+' in Ally')
            # print(ticker[0] + "not"+str(ticker[3])+ " in " + account + "in ally")


def fidelityLogin():
    try:
        driver.get(
            "https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://digital.fidelity.com/ftgw/digital/portfolio/summary"
        )
        slowSleep()
        driver.find_element(By.CSS_SELECTOR, ".main-container").click()
        driver.find_element(By.CSS_SELECTOR, ".pvd-button__contents").click()
    except:
        loginLog("Fidelity")


def fidelityExec(accounts, tickers):
    for account in accounts:
        for ticker in tickers:
            try:
                if ticker[3]:
                    act = "B"
                else:
                    act = "S"
                driver.get(
                    "https://digital.fidelity.com/ftgw/digital/trade-equity/index?ORDER_TYPE=E&ACCOUNT="
                    + account
                    + "&SYMBOL="
                    + ticker[0]
                    + "&PRICE_TYPE=L&ORDER_ACTION="
                    + act
                    + "&QTY="
                    + str(ticker[2])
                )  #
                slowSleep()
                # set limit price
                driver.find_element(By.ID, "eqt-mts-limit-price").send_keys(ticker[1])
                fastSleep()
                # preview
                driver.find_element(
                    By.CSS_SELECTOR, "#previewOrderBtn .pvd3-button-root"
                ).click()
                slowSleep()
                # place
                driver.find_element(By.ID, "placeOrderBtn").click()
                goodDB(ticker, account + " in Fidelity")
            except:
                errorLog(ticker, account + " in Fidelity")


def firstradeLogin():
    try:
        driver.get("https://invest.firstrade.com/cgi-bin/login")
        slowSleep()
        driver.find_element(By.ID, "loginButton").click()
    except:
        loginLog("Firstrade")


def firstradeExec(accounts, tickers):
    driver.get("https://invest.firstrade.com/cgi-bin/main#/cgi-bin/stock_order")
    slowSleep()
    for account in accounts:
        try:
            Select(driver.find_element(By.ID, "accountId1")).select_by_visible_text(
                account
            )
            fastSleep()
        except:
            print("change account failed")
        for ticker in tickers:
            try:
                if ticker[3]:
                    driver.find_element(By.ID, "transactionType_Buy1").click()
                else:
                    driver.find_element(By.ID, "transactionType_Sell1").click()
                # quantity
                driver.find_element(By.ID, "quantity1").send_keys(ticker[2])
                # ticker
                driver.find_element(By.ID, "symbol1").send_keys(ticker[0])
                driver.find_element(By.ID, "limitPrice1").click()
                # submit
                slowSleep()
                driver.find_element(By.ID, "submitOrder1").click()
                # place another
                slowSleep()
                driver.find_element(
                    By.CSS_SELECTOR, ".submitted_placeorder_bnt"
                ).click()
                fastSleep()
                goodDB(ticker, account + " in Firstrade")
            except:
                errorLog(ticker, account + " in Firstrade")
                # print(ticker[0] + "not"+str(ticker[3])+ " in " + account + "in firstrade")


# TODO sell
def publicExec(tickers):
    for ticker in tickers:
        try:
            driver.get("https://public.com/stocks/" + ticker[0])
            shares = int(math.ceil(1 / ticker[1]))
            if shares < ticker[2]:
                shares = ticker[2]
            slowSleep()
            # click buy is default                      /html/body/div/div[1]/div/div/div[2]/div/main/div/div[2]/div[1]/div/div[2]/div/label[2]/span
            driver.find_element(
                By.XPATH,
                "//*[@id='maincontent']/div/div[2]/div[1]/div/div/div/button[1]/span",
            ).click()
            fastSleep()
            driver.find_element(
                By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[1]/div/button"
            ).click()
            fastSleep()
            driver.find_element(
                By.XPATH,
                "/html/body/div[11]/div[3]/div/div/div/div/div[1]/div/div/button[2]",
            ).click()
            fastSleep()
            driver.find_element(
                By.XPATH,
                "/html/body/div[11]/div[3]/div/div/div/div/div[4]/div[1]/div/div[1]/input",
            ).send_keys(shares)
            fastSleep()
            driver.find_element(
                By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[5]/button"
            ).click()
            fastSleep()
            driver.find_element(
                By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[3]/button"
            ).click()
            fastSleep()
            driver.find_element(
                By.XPATH, "/html/body/div[11]/div[3]/div/div/div/div/div[2]/button"
            ).click()
            goodDB(ticker, "Public")
        except:
            errorLog(ticker, "Public")
            # print(ticker[0] + "not"+str(ticker[3])+ " in public")


def robinhoodLogin():
    try:
        driver.get("https://robinhood.com/login")
        slowSleep()
        driver.find_element(By.XPATH, "//*[@id='submitbutton']/div/button").click()
    except:
        loginLog("Robinhood")


def robinhoodExec(accounts, tickers):
    for ticker in tickers:
        driver.get("https://robinhood.com/stocks/" + ticker[0])
        slowSleep()
        for account in accounts:
            # try:
            # change account
            driver.find_element(By.XPATH, "//form/button").click()
            driver.find_element(By.XPATH, "//p[contains(.,'" + account + "')]").click()
            if not ticker[3]:
                driver.find_element(By.XPATH, "//span[contains(.,'Sell')]").click()
                fastSleep()
            # quantity
            driver.find_element(By.NAME, "quantity").click()
            fastSleep()
            driver.find_element(By.NAME, "quantity").send_keys("1")
            fastSleep()
            # review order
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            slowSleep()
            # submit
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            slowSleep()
            # done
            driver.find_element(By.XPATH, "//button[contains(.,'Done')]").click()
            slowSleep()
            goodDB(ticker, account + " in Robinhood")
            # except:
            # errorLog(ticker,account+' in Robinhood')
            # print(ticker[0] + "not"+str(ticker[3])+ " in " + str(i) + "in robinhood")


def schwabLogin():
    # schwab login page
    try:
        driver.get("https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx")

        iframe = driver.find_element(By.ID, "lmsSecondaryLogin")
        driver.switch_to.frame(iframe)

        # wait for autocomplete
        slowSleep()
        driver.find_element(By.ID, "btnLogin").click()
    except:
        loginLog("Schwab")


# TODO quantity > 1
def schwabExec(accounts, tickers):
    driver.get("https://client.schwab.com/app/trade/tom/#/trade")
    slowSleep()
    # loop through accounts
    for account in accounts:
        driver.find_element(By.XPATH, "//sdps-account-selector/div/div/button").click()
        print(account)
        driver.find_element(By.XPATH, "//span[contains(.,'" + account + "')]").click()

        # loop through tickers
        for ticker in tickers:
            try:
                slowSleep()
                tickerBox = driver.find_element(By.ID, "_txtSymbol")
                tickerBox.send_keys(ticker[0])
                tickerBox.send_keys(Keys.ENTER)
                fastSleep()
                # action
                actionBox = Select(driver.find_element(By.ID, "_action"))
                if ticker[3]:
                    # buy
                    actionBox.select_by_visible_text("Buy")
                else:
                    # sell
                    actionBox.select_by_visible_text("Sell")

                # quantity
                # ticker[2]
                # TODO

                # review
                driver.find_element(By.CSS_SELECTOR, ".mcaio-order--reviewbtn").click()
                # place
                slowSleep()
                driver.find_element(By.ID, "mtt-place-button").click()
                # place another
                slowSleep()
                driver.find_element(
                    By.CSS_SELECTOR, ".mcaio--mcaio-cta-buttons-anothertrade"
                ).click()
                goodDB(ticker, account + " in Schwab")
            except:
                errorLog(ticker, account + " in Schwab")


# TODO
def sofiLogin():
    driver.get("https://sofi.com/login")
    return


# TODO setup sell
def sofiExec(accounts, tickers):
    for ticker in tickers:
        driver.get("https://www.sofi.com/wealth/app/stock/" + ticker[0])
        for account in range(accounts):
            try:
                slowSleep()
                buy = driver.find_element(
                    By.XPATH,
                    "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button",
                )
                if not (buy.is_enabled()):
                    print("not on SOFI")
                    return
                driver.find_element(
                    By.XPATH,
                    "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button",
                ).click()
                fastSleep()
                Select(
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[1]/div/select",
                    )
                ).select_by_visible_text(account)
                fastSleep()
                driver.find_element(
                    By.XPATH,
                    "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/input",
                ).send_keys(ticker[2])
                driver.find_element(
                    By.XPATH,
                    "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[4]/div[2]/input",
                ).send_keys(ticker[1])
                driver.find_element(
                    By.CSS_SELECTOR, ".StyledActionButton-hdOdyk"
                ).click()
                slowSleep()
                driver.find_element(
                    By.CSS_SELECTOR, ".StyledActionButton-hdOdyk"
                ).click()
                fastSleep()
                driver.find_element(
                    By.XPATH,
                    "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/button",
                ).click()
                goodDB(ticker, account + " in Sofi")
            except:
                errorLog(ticker, account + " in Sofi")
                # print(ticker[0] + "not"+str(ticker[3])+ " in " + str(account) + "in sofi")


def tradierExec(accounts, tickers):
    tradierToken = accounts[0]
    accounts = accounts[1:]
    for account in accounts:
        for ticker in tickers:
            if ticker[3]:
                side = "buy"
            else:
                side = "sell"
            headers = {
                "Authorization": "Bearer {}".format(tradierToken),
                "Accept": "application/json",
            }
            url = "https://api.tradier.com/v1/accounts/{}/orders".format(account)
            response = requests.post(
                url,
                data={
                    "class": "equity",
                    "symbol": ticker[0],
                    "side": side,
                    "quantity": ticker[2],
                    "type": "market",
                    "duration": "day",
                },
                headers=headers,
            )
            json_response = response.json()
            goodDB(ticker, account + " in Tradier")


def vanguardLogin():
    try:
        driver.get("https://holdings.web.vanguard.com/")
        slowSleep()
        driver.find_element(
            By.XPATH, "//*[@id='username-password-submit-btn-1']"
        ).click()
    except:
        loginLog("Vanguard")


def vanguardExec(accounts, tickers):
    qqq = 0
    # loop through accounts
    for account in accounts:
        qqq = qqq + 1
        print(qqq)
        for ticker in tickers:
            try:
                driver.get(
                    "https://personal.vanguard.com/us/buysell/web/tradeticket/TradeTicket.xhtml?investmentType=EQUITY"
                )
                slowSleep()
                # chnage account
                driver.execute_script(
                    "const xpath = '/html/body/div[3]/div[5]/span/div/span[3]/div/div[1]/div/div[2]/div/span/span[2]/div/div/div[1]/span/div/p[1]/b'; const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (element && element.textContent === 'Incomplete transaction detected') {    const okButton = document.getElementById('okButtonInput');    if (okButton) {        okButton.click();    } } "
                )
                fastSleep()
                driver.find_element(By.ID, "baseForm:accountSelectOne_text").click()
                # driver.execute_script("return !(document.querySelector('.vg-SelOneMenuFocusText'));")
                test = driver.find_element(
                    By.ID, "baseForm:accountSelectOne:" + str(qqq)
                ).click()
                # action
                fastSleep()
                driver.find_element(By.ID, "baseForm:transactionTypeSelectOne").click()
                fastSleep()
                if ticker[3]:
                    driver.find_element(
                        By.ID, "baseForm:transactionTypeSelectOne:1"
                    ).click()
                else:
                    driver.find_element(
                        By.ID, "baseForm:transactionTypeSelectOne:2"
                    ).click()
                fastSleep()
                # ticker
                tickerBox = driver.find_element(By.ID, "baseForm:investmentTextField")
                # ticker.click()
                tickerBox.send_keys(ticker[0])
                # sleep(5)
                # quantity
                driver.find_element(By.ID, "baseForm:shareQuantityTextField").click()
                fastSleep()
                driver.execute_script(
                    "input = document.getElementById('baseForm:shareQuantityTextField'); input.select(); input.value='"
                    + str(ticker[2])
                    + "'; input.setAttribute('value', input.value);"
                )

                # order type
                driver.find_element(By.ID, "baseForm:orderTypeSelectOne_text").click()
                fastSleep()
                driver.find_element(By.ID, "baseForm:orderTypeSelectOne:2").click()

                # limit price
                # driver.find_element(By.ID, "baseForm:limitPriceTextField").click()
                fastSleep()
                driver.execute_script(
                    "input = document.getElementById('baseForm:limitPriceTextField'); input.select(); input.value='"
                    + str(ticker[1])
                    + "'; input.setAttribute('value', input.value);"
                )

                # duration
                driver.find_element(
                    By.ID, "baseForm:durationTypeSelectOne_text"
                ).click()
                fastSleep()
                driver.find_element(By.ID, "baseForm:durationTypeSelectOne:1").click()
                # cost basis
                if not ticker[3] and account == 0:
                    driver.find_element(
                        By.ID, "baseForm:costBasisMethodSelectOne_main"
                    ).click()
                    fastSleep()
                    driver.find_element(
                        By.ID, "baseForm:costBasisMethodSelectOne:1"
                    ).click()
                # continue
                driver.find_element(By.ID, "baseForm:reviewButtonInput").click()
                slowSleep()
                # submit
                driver.find_element(By.ID, "baseForm:submitButtonInput").click()
                fastSleep()
                goodDB(ticker, account + " in Vanguard")
            except:
                errorLog(ticker, account + " in Vanguard")


def wellsFargoLogin():
    try:
        driver.get("https://connect.secure.wellsfargo.com/auth/login/present")
        slowSleep()
        login = driver.find_element(By.CSS_SELECTOR, ".Button__modern___cqCp7")
        login.click()
    except:
        loginLog("WellsFargo")


def wellsFargoExec(accounts, tickers):
    # navigate to it cuz wellsfargo got weird links
    try:
        driver.find_element(By.XPATH, "//*[@id='BROKERAGE_LINK7P']").click()
        slowSleep()
        driver.find_element(By.XPATH, "//*[@id='trademenu']/span[1]").click()
        slowSleep()
        driver.find_element(By.XPATH, "//*[@id='linktradestocks']").click()
        fastSleep()
        driver.find_element(By.XPATH, "//*[@id='dropdown2']").click()
        fastSleep()
        driver.find_element(By.XPATH, "//*[@id='dropdownlist2']/li[1]").click()
        fastSleep()
    except:
        print("navigation failed")
    # driver.execute_script("document.body.style.zoom = '0.5'")
    # this kills it TODO fix manualy zoom out for now

    for i in range(accounts):
        try:
            driver.find_element(By.XPATH, "//*[@id='dropdown2']").click()
            fastSleep()
            driver.find_element(
                By.XPATH, "//*[@id='dropdownlist2']/li[" + str(i + 1) + "]"
            ).click()
            fastSleep()
            driver.find_element(By.XPATH, "//*[@id='btn-continue']").click()
        except:
            print("changing account failed")
        for ticker in tickers:
            try:
                # action
                # driver.find_element(By.ID, "BuySellBtn").click()
                driver.execute_script('document.getElementById("BuySellBtn").click()')
                if ticker[3]:
                    driver.find_element(By.LINK_TEXT, "Buy").click()
                else:
                    action = driver.find_element(By.LINK_TEXT, "Sell")
                    action.click()

                # ticker
                tickerBox = driver.find_element(By.ID, "Symbol")
                tickerBox.send_keys(ticker[0])
                tickerBox.send_keys(Keys.ENTER)

                fastSleep()
                # quantity
                tickerBox = driver.find_element(By.ID, "OrderQuantity")
                tickerBox.send_keys(ticker[2])
                tickerBox.send_keys(Keys.ENTER)

                # order type
                orderBox = driver.find_element(By.ID, "OrderTypeBtnText")
                orderBox.click()
                fastSleep()
                order = driver.find_element(By.LINK_TEXT, "Limit")
                order.click()

                # limit price
                tickerBox = driver.find_element(By.ID, "Price")
                tickerBox.send_keys(ticker[1])
                tickerBox.send_keys(Keys.ENTER)

                # timing
                driver.find_element(By.ID, "TIFBtn").click()
                fastSleep()
                driver.find_element(By.LINK_TEXT, "Day").click()

                # preview
                fastSleep()
                review = driver.find_element(By.ID, "actionbtnContinue")
                review.click()
                slowSleep()
                # submit
                submit = driver.find_element(By.CSS_SELECTOR, ".btn-wfa-submit")
                submit.click()
                slowSleep()
                driver.find_element(By.CSS_SELECTOR, ".btn-wfa-primary").click()
                goodDB(ticker, str(i) + " in Wells Fargo")
            except:
                errorLog(ticker, str(i) + " in Wells Fargo")
                # print(ticker[0] + "not"+str(ticker[3])+ " in " + str(i) + "in wells fargo")
