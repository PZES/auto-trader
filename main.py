import tkinter as tk
from tkinter import messagebox, Text
from auto import *
from data import accounts
from helpers import setTickers


def authenticatePlatform(platform, tickers):
    # Perform platform-specific login
    if loginFunctions[platform] is not None:
        loginFunctions[platform]()

    # Create a tkinter Toplevel window for authentication confirmation
    authWindow = tk.Toplevel(root)
    authWindow.title(f"Authenticate {platform}")

    # Label and Entry widget for user confirmation
    tk.Label(authWindow, text=f"Press Enter to authenticate {platform}").pack(pady=10)
    entry = tk.Entry(authWindow)
    entry.pack(pady=5)

    # Function to handle Enter key press
    def onEnter(event=None):
        authWindow.destroy()  # Close the authentication window
        executeFunctions[platform](accounts[platform], tickers)

    # Bind Enter key press to call onEnter function
    entry.bind("<Return>", lambda event: onEnter())

    # Focus on the Entry widget and start tkinter main loop for authentication
    entry.focus_set()
    authWindow.mainloop()


def displayLog():
    try:
        with open("data.log", "r") as f:
            logContent = f.read()
            textLog.delete("1.0", tk.END)  # Clear previous content
            textLog.insert(tk.END, logContent)  # Insert log content into Text widget

            # Auto-scroll to the end of the Text widget
            textLog.see(tk.END)

    except FileNotFoundError:
        messagebox.showerror("File Error", "Log file not found.")

    # Schedule the next update after 1 second (1000 milliseconds)
    textLog.after(1000, displayLog)


def runSelectedPlatforms():
    selectedPlatforms = [
        platform for platform, var in checkboxes.items() if var.get() == 1
    ]
    tickersInput = entryTickers.get("1.0", tk.END)  # Get tickers input from Text widget

    if not tickersInput.strip():
        messagebox.showerror("Error", "Please enter tickers before proceeding.")
        return
    tickers = setTickers(tickersInput)
    for platform in selectedPlatforms:
        authenticatePlatform(platform, tickers)


def createMainWindow():
    global root, entryTickers, textLog, checkboxes

    # Create tkinter window
    root = tk.Tk()
    root.title("Auto Trader")

    # Instructions and Example for user input
    instructionText = "Enter 'b' or 's' followed by ticker symbol (one per line):\nExample:\nb\nAAPL\nQQQ\nGME\ns\nNVDA\nGOOG"
    tk.Label(root, text=instructionText, justify=tk.LEFT).pack(pady=5)

    # Example tickers entry with Text widget for multiline input
    entryTickers = tk.Text(root, height=10, width=30)
    entryTickers.pack(pady=5)

    # Create checkboxes for each platform
    platforms = [
        "Ally",
        "Fidelity",
        "Firstrade",
        "Public",
        "Robinhood",
        "Schwab",
        "SoFi",
        "Tradier",
        "Vanguard",
        "WellsFargo",
    ]

    checkboxes = {}
    for platform in platforms:
        var = tk.IntVar()
        chk = tk.Checkbutton(root, text=platform, variable=var, onvalue=1, offvalue=0)
        chk.pack(anchor=tk.W)
        checkboxes[platform] = var

    # Create "Run" button
    btnRun = tk.Button(root, text="Run", command=runSelectedPlatforms)
    btnRun.pack(pady=10)

    # Text widget to display log content
    textLog = tk.Text(root, height=10, width=50)
    textLog.pack(pady=10)

    displayLog()

    # Run the tkinter main loop
    root.mainloop()


# Define login and execute functions for each platform
loginFunctions = {
    "Ally": allyLogin,
    "Fidelity": fidelityLogin,
    "Firstrade": firstradeLogin,
    "Public": None,
    "Robinhood": robinhoodLogin,
    "Schwab": schwabLogin,
    "SoFi": sofiLogin,
    "Tradier": None,
    "Vanguard": vanguardLogin,
    "WellsFargo": wellsFargoLogin,
}

executeFunctions = {
    "Ally": allyExec,
    "Fidelity": fidelityExec,
    "Firstrade": firstradeExec,
    "Public": publicExec,
    "Robinhood": robinhoodExec,
    "Schwab": schwabExec,
    "SoFi": sofiExec,
    "Tradier": tradierExec,
    "Vanguard": vanguardExec,
    "WellsFargo": wellsFargoExec,
}

# Start the application
createMainWindow()
