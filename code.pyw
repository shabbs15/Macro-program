import os
import webbrowser
import subprocess
import sys

import tkinter as tk
import tkinter.font as tkFont
import json

jsonFile = open("macro.json")
jsonString = jsonFile.read()
jsonData = json.loads(jsonString)

chrome_path = jsonData["chrome_path"]

def launchingItems(value):
    if len(value["websites"]) != 0:
        subprocess.Popen(chrome_path, shell=True)

    for i in value["programs"]:
        os.startfile(i)

    if len(value["websites"]) != 0:
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

        chrome = webbrowser.get("chrome")

        for i in value["websites"]:
            chrome.open(i)

def keyPress(event):
    stroke = event.keysym.lower()
    if stroke == "escape":
        window.destroy()
        sys.exit()
    else:
        for key,value in jsonData["macros"].items():
            if stroke == value["code"].lower():
                launchingItems(value)
                break


window = tk.Tk()
fontO = tkFont.Font(family = "Segoe Ui", size = 11)

window.option_add( "*font", fontO)

windowWidth = 300
windowHeight = 200

windowX = (window.winfo_screenwidth()/2) - (windowWidth/2)
windowY = (window.winfo_screenheight()/2) - (windowHeight/2)

window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, windowX, windowY ))

escape = tk.Label(text = "Esc to close window \n", font =("Segoe UI",11, "bold") )
escape.pack()

for key,value in jsonData["macros"].items():

    framo = tk.Frame(window)
    framo.pack(fill = tk.X)

    labo = tk.Label(framo,text = value["code"] +": " + value["name"])
    labo.pack()

window.bind("<KeyPress>",keyPress)

window.mainloop()
