from auto import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import data
from helpers import setTickers
Buy = True
Sell = False

window = tk.Tk()
window.title("Auto Trader")


####### change this command in windows ########
#def openChrome():
#    os.system("google-chrome-stable --remote-debugging-port=9222 &")


#TODO set ability to buy and sell tickers

allyVar = BooleanVar()
fidelityVar = BooleanVar()
firstradeVar = BooleanVar()
publicVar = BooleanVar()
robinhoodVar = BooleanVar()
schwabVar = BooleanVar()
sofiVar = BooleanVar()
tradierVar = BooleanVar()
vanguardVar = BooleanVar()
wellsVar = BooleanVar()
    
def run():
    tickers = T.get(1.0, "end-1c") 
    tickers = setTickers(tickers)
  
    if(fidelityVar.get()):
        print("1")
        fidelityLogin()
        input("Press enter after Authentication")
        fidelityExec(data.fidelityAccounts, tickers)
    if(firstradeVar.get()):
        print("1")
        firstradeLogin()
        input("Press enter after Authentication")
        firstradeExec(data.firstradeAccounts,tickers)
    if(publicVar.get()):
        print("1")
        publicExec(tickers)
    if(robinhoodVar.get()):
        print("1")
        robinhoodLogin()
        input("Press enter after Authentication")
        #TODO dint work
        robinhoodExec(data.RobinhoodAccounts, tickers)
    if(schwabVar.get()):
        print("1")
        #schwabLogin()
        input("Press enter after Authentication")
        schwabExec(data.numOfSchwabAccounts,tickers)
    if(sofiVar.get()):
        print("1")
        sofiLogin()
        #TODO breaks after one not in
        input("Press enter after Authentication")
        sofiExec(data.numOfSOFIAccounts, tickers)
    if(tradierVar.get()):
        print("1")
        tradierExec(data.tradierAccounts, tickers, data.tradierToken)
    if(vanguardVar.get()):
        print("1")
        vanguardLogin()
        input("Press enter after Authentication")
        vanguardExec(data.numOfVanguardAccounts, tickers)
    if(wellsVar.get()):
        print("1")
        wellsFargoLogin()
        input("Press enter after Authentication")
        wellsFargoExec(data.numOfWellsAccounts, tickers)
    if(allyVar.get()):
        print("1")
        allyLogin()
        input("Press enter after Authentication")
        allyExec(data.allyAccounts, tickers)



Checkbutton(text="fidelity", variable = fidelityVar)
Checkbutton(text="firstrade", variable = firstradeVar)
Checkbutton(text="public", variable = publicVar)
Checkbutton(text="robinhood", variable = robinhoodVar)
Checkbutton(text="schwab", variable = schwabVar)
Checkbutton(text="sofi", variable = sofiVar)
Checkbutton(text="tradier", variable = tradierVar)
Checkbutton(text="vanguard", variable = vanguardVar)
Checkbutton(text="wells", variable = wellsVar)
Checkbutton(text="ally", variable = allyVar)

Label(window, text = "How to add stocks to buy/sell")
Label(window, text = "Write every tiker in new line")
Label(window, text = "Ticker,Price,Amount,Buy/Sell")
Label(window, text = "Ex:")
Label(window, text = "SPY,500.00,50,Buy")
Label(window, text = "QQQ,400.00,10,Sell")

T = Text(window, height = 10, width = 50)
Button(window, text="Run", command= run)

for c in sorted(window.children):
    window.children[c].pack()


window.mainloop()


#allyLogin()
#input("Press enter after Authentication")
#allyExec(allyAccounts, tickers)
#fidelityLogin()
#input("Press enter after Authentication")
#fidelityExec(fidelityAccounts, tickers)
#firstradeLogin()
#input("Press enter after Authentication")
#firstradeExec(firstradeAccounts,tickers)
#publicExec(tickers)
#robinhoodLogin()
#input("Press enter after Authentication")
#TODO dint work
#robinhoodExec(RobinhoodAccounts, tickers)
#schwabLogin()
#input("Press enter after Authentication")
#schwabExec(numOfSchwabAccounts,tickers)
#sofiLogin()
#TODO breaks after one not in
#input("Press enter after Authentication")
#sofiExec(numOfSOFIAccounts, tickers)
#tradierExec(tradierAccounts, tickers, tradierToken)
#vanguardLogin()
#input("Press enter after Authentication")
#vanguardExec(numOfVanguardAccounts, tickers)
#wellsFargoLogin()
#input("Press enter after Authentication")
#TODO zoom out
#wellsFargoExec(numOfWellsAccounts, tickers)
