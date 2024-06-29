import tkinter as tk
from tkinter import messagebox, Text
from auto import *
from data import accounts
from helpers import setTickers


# google-chrome-stable --remote-debugging-port=9222
def authenticate_platform(platform, tickers):
    # Perform platform-specific login
    if login_functions[platform] is not None:
        login_functions[platform]()

    # Create a tkinter Toplevel window for authentication confirmation
    auth_window = tk.Toplevel(root)
    auth_window.title(f"Authenticate {platform}")

    # Label and Entry widget for user confirmation
    tk.Label(auth_window, text=f"Press Enter to authenticate {platform}").pack(pady=10)
    entry = tk.Entry(auth_window)
    entry.pack(pady=5)

    # Function to handle Enter key press
    def on_enter(event=None):
        auth_window.destroy()  # Close the authentication window
        execute_functions[platform](accounts[platform], tickers)

    # Bind Enter key press to call on_enter function
    entry.bind("<Return>", lambda event: on_enter())

    # Focus on the Entry widget and start tkinter main loop for authentication
    entry.focus_set()
    auth_window.mainloop()


def display_log():
    try:
        with open("data.log", "r") as f:
            log_content = f.read()
            text_log.delete("1.0", tk.END)  # Clear previous content
            text_log.insert(tk.END, log_content)  # Insert log content into Text widget

            # Auto-scroll to the end of the Text widget
            text_log.see(tk.END)

    except FileNotFoundError:
        messagebox.showerror("File Error", "Log file not found.")

    # Schedule the next update after 1 second (1000 milliseconds)
    text_log.after(1000, display_log)


def run_selected_platforms():
    selectedPlatforms = [
        platform for platform, var in checkboxes.items() if var.get() == 1
    ]
    tickersInput = entry_tickers.get(
        "1.0", tk.END
    )  # Get tickers input from Text widget

    if not tickersInput.strip():
        messagebox.showerror("Error", "Please enter tickers before proceeding.")
        return
    print(tickersInput)
    tickers = setTickers(tickersInput)
    print(tickers)
    for platform in selectedPlatforms:
        authenticate_platform(platform, tickers)


# Create tkinter window
root = tk.Tk()
root.title("Platform Operations")

# Instructions and Example for user input
instruction_text = "Enter 'b' or 's' followed by ticker symbol (one per line):\nExample:\nb\nAAPL\nQQQ\nGME\ns\nNVDA\nGOOG"
tk.Label(root, text=instruction_text, justify=tk.LEFT).pack(pady=5)

# Example tickers entry with Text widget for multiline input
entry_tickers = tk.Text(root, height=10, width=30)
entry_tickers.pack(pady=5)

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

login_functions = {
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

execute_functions = {
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

checkboxes = {}
for platform in platforms:
    var = tk.IntVar()
    chk = tk.Checkbutton(root, text=platform, variable=var, onvalue=1, offvalue=0)
    chk.pack(anchor=tk.W)
    checkboxes[platform] = var

# Create "Run" button
btn_run = tk.Button(root, text="Run", command=run_selected_platforms)
btn_run.pack(pady=10)

# Text widget to display log content
text_log = tk.Text(root, height=10, width=50)
text_log.pack(pady=10)

display_log()

# Run the tkinter main loop
root.mainloop()
