from auto import *


Buy = True
Sell = False


#this is ur tradier api
tradierToken = 'fillthisout' 

numOfSchwabAccounts = 3
numOfRobinhoodAccounts = 3
numOfSOFIAccounts = 3
numOfVanguardAccounts = 3
numOfWellsAccounts = 3
#Fill list with how much ever account you have
firstradeAccounts = ["00000000-Name", "00000000-Nick"]
allyAccounts = ["Full Name-0000", "Full Name-0000"]
tradierAccounts = ["0X0X0X0X", "0X0X0X0X"] #ACCOUNT NUMBER
fidelityAccounts = ["X0X0X0X0X", "X0X0X0X0X"] #ACCOUNT NUMBER
#fidelity margin not yet supported
sofiAccounts = ["Full Name", "Full Name"]

#currently only one ticker at a time
tickers = ['PAVM']
action = Buy
quantity = 1
price = 0.25


allyLogin()
allyExec(allyAccounts, tickers, action, quantity)
#fidelityLogin()
fidelityExec(fidelityAccounts, tickers,action,quantity, price)
firstradeLogin()
firstradeExec(firstradeAccounts,tickers,action,quantity)
publicExec(tickers,action,quantity,price)
#robinhoodLogin()
robinhoodExec(numOfRobinhoodAccounts, tickers, action, quantity)
schwabLogin()
schwabExec(numOfSchwabAccounts,tickers,action,quantity)
#sofiLogin()
sofiExec(numOfSOFIAccounts, tickers,action,quantity,price)
stocktwitsExec(tickers,action,quantity)
tradierExec(tradierAccounts, tickers, action, quantity, tradierToken)
#vanguardLogin()
vanguardExec(numOfVanguardAccounts, tickers, action, quantity, price)
wellsFargoLogin()
wellsFargoExec(numOfWellsAccounts, tickers, action, quantity, price)
