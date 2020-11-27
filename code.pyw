import os
import webbrowser
import subprocess
import sys

import tkinter as tk
import tkinter.font as tkFont
import json

from functools import partial

jsonFile = open("macro.json")
jsonString = jsonFile.read()
jsonData = json.loads(jsonString)

chrome_path= jsonData["chrome_path"] #initalizes chrome path

windowWidth = 400 #sets window width
windowHeight = 300 #sets window high

window = tk.Tk() #creates root window

fontO = tkFont.Font(family = "Segoe Ui", size = 11)
window.option_add( "*font", fontO) #default font

fontSmall = tkFont.Font(family = "Segoe Ui", size = 10,underline = True) #font for buttons
fontBold = tkFont.Font(family = "Segoe UI",size = 11, weight = "bold")

window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, 20,20)) #generates window

#creates frame for enter code
enterCodeFrame = tk.Frame(window)
enterCodeFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

codeEntry = tk.Entry(enterCodeFrame,justify = "center")
codeEntry.type = "code"

codeEntry.insert("end", 'Enter code for new macro')
codeEntry.defaultInput = True
codeEntry.pack(fill = tk.X)

def launchingItems(value): #launches websites and programs in a macro
    if len(value["websites"]) != 0:
        subprocess.Popen(chrome_path, shell=True) #crates new window

    for i in value["programs"]:
        os.startfile(i) #loops programs

    if len(value["websites"]) != 0:
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

        chrome = webbrowser.get("chrome")

        for i in value["websites"]: #launches websites
            chrome.open(i)

def keyPress(event): #callback for keystrokes
    stroke = event.keysym.lower() #lowercase
    foc = window.focus_get() #gets the widget which is currently active (entry, button etc.)

    if stroke == "escape": #closes program
        window.destroy()
        sys.exit()

    if not foc.winfo_class() == "Entry": #if not entry, assumes macro stroke
        for key,value in jsonData["macros"].items(): #loops through macro codes checking strokes
            if stroke == value["code"].lower():
                launchingItems(value)
                break
    elif stroke == "return": #this is entry
        link = foc.get() #gets text in entry

        if foc.type == "sub": #entry for website or program
            if os.path.exists(link): # adds program to json
                print("path found")
                foc.delete("0","end")
                foc.insert("0","")

                jsonData["macros"][foc.MacroName]["programs"].append(link)

                updateJsonFunction()
                buttonCommand(foc.MacroName)
            elif "." in link: #adds website to json
                foc.delete("0","end")
                foc.insert("0","")

                jsonData["macros"][foc.MacroName]["websites"].append(link)

                updateJsonFunction()
                buttonCommand(foc.MacroName)
        elif foc.type == "main": #checks if new macro is being created
            foc.delete("0","end")
            foc.insert("0","")

            createNewMacro(link)
        elif foc.type == "code": #checks if code for macro is being created
            if len(link) == 1:
                codeRepeatCheck = False #checks for code repeats
                for key,value in jsonData["macros"].items():
                    if value["code"] == link:
                        codeRepeatCheck = True
                        break
                if codeRepeatCheck == False: #adds to json to program
                    jsonData["macros"][foc.MacroName] = {
                        "code": link,
                        "name": foc.MacroName,
                        "programs": [],
                        "websites":[]
                    }

                    buttonCommand(foc.MacroName)
                    updateJsonFunction()

    elif foc.defaultInput == True:
        if stroke == "backspace": #removes default text once backpressed pressed
            foc.defaultInput = False
            foc.delete("0","end")
            foc.insert("0","")

def createNewMacro(link): #name of macro is stored in entry which inputs code
    codeEntry.MacroName = link
    enterCodeFrame.tkraise()

def buttonCommand(macro): #creates window when user is editting macro

    newFrame = tk.Frame(window) #master frame
    newFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    framo = tk.Frame(newFrame)
    framo.pack(fill = tk.X)

    escape = tk.Label(newFrame,text = "Websites \n", font =fontBold )
    escape.pack(fill = tk.X)

    genre = "websites" #loops through list of websites and creates label

    for key,value in enumerate(jsonData["macros"][macro][genre]):
        framo = tk.Frame(newFrame)
        framo.pack(fill = tk.X)

        labo = tk.Label(framo, text = value)
        labo.pack()

        args = [key,macro,genre]
        actionArg = partial(deleteItem,args)

        futon = tk.Button(framo, text = "Delete", command = actionArg, borderwidth = 0, font = fontSmall, cursor ="hand2", height = 0, width = 5)
        futon.place(relx=1, x=-2,rely = 0.5, anchor=tk.E)

    escape = tk.Label(newFrame,text = "Programs \n", font =fontBold )
    escape.pack(fill = tk.X)

    genre = "programs" #loops through programs and creates label

    for key,value in enumerate(jsonData["macros"][macro][genre]):

        framo = tk.Frame(newFrame)
        framo.pack(fill = tk.X)

        labo = tk.Label(framo, text = value)
        labo.pack()

        args = [key,macro,genre]
        actionArg = partial(deleteItem,args)

        futon = tk.Button(framo, text = "Delete", command = actionArg, borderwidth = 0, font = fontSmall, cursor ="hand2", height = 0, width = 5)
        futon.place(relx=1, x=-2,rely = 0.5, anchor=tk.E)

    # entry textbook to input new website or file location
    textBox = tk.Entry(newFrame, justify = "center")
    textBox.insert("end", 'Type new website or file location here')
    textBox.MacroName = macro
    textBox.defaultInput = True
    textBox.type = "sub"
    textBox.pack(fill = tk.X)

    deletePartial = partial(macroDeletion,macro)

    completeDeletion = tk.Button(newFrame, text = "Delete Macro", command = deletePartial, borderwidth = 0, font = fontSmall, cursor ="hand2", height = 0, width = 5)
    completeDeletion.pack(fill = tk.X) #button to delete macro

    futon = tk.Button(newFrame, text = "Return", command = mainWindowLaunch, borderwidth = 0, font = fontSmall, cursor ="hand2", height = 0, width = 5)
    futon.pack(fill = tk.X) # button to go to main window

    newFrame.tkraise()
def updateJsonFunction(): # updates file from json variable
    with open("macro.json","w") as fp:
        json.dump(jsonData,fp, sort_keys=True, indent=4)

def deleteItem(args): # deletes program or website from macro
    key = args[0]#position
    macro = args[1]
    genre = args[2] #if website or program

    del jsonData["macros"][macro][genre][key]

    updateJsonFunction()

    buttonCommand(macro)

def macroDeletion(macro): # deletes macro, launches main window
    del jsonData["macros"][macro]

    updateJsonFunction()
    mainWindowLaunch()

def mainWindowLaunch():

    mainWindowFrame = tk.Frame(window) #main frame
    mainWindowFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    framo = tk.Frame(mainWindowFrame)
    framo.pack(fill = tk.BOTH, side = "top")

    escape = tk.Label(framo,text = "Esc to close window \n", font =fontBold)
    escape.pack(fill = tk.X)

    for key,value in jsonData["macros"].items():
        framo = tk.Frame(mainWindowFrame)
        framo.pack(fill = tk.X, side = "top")

        labo = tk.Label(framo,text = value["code"] +": " + value["name"])
        labo.pack()

        actionArg = partial(buttonCommand,value["name"])

        button = tk.Button(framo, text = "Edit", command = actionArg, borderwidth = 0, font = fontSmall, cursor ="hand2", height = 0, width = 3)
        button.place(relx=1, x=-2,rely = 0.5, anchor=tk.E)

    #entry for new macro
    textBox = tk.Entry(mainWindowFrame, justify = "center")
    textBox.insert("end", 'Enter new macro name')
    textBox.type = "main"
    textBox.defaultInput = True
    textBox.pack(fill = tk.X)

    mainWindowFrame.tkraise()

def mouseClick(arg): # entry can be deselected when clicked elsewhere
    print(arg.widget.winfo_class())
    print("current", window.focus_get().winfo_class())


    if not arg.widget.winfo_class() == "Button":
        print(arg.widget.winfo_class())
        arg.widget.focus_set()
    elif window.focus_get().winfo_class() == "Entry":
        print(arg.widget.winfo_class())
        arg.widget.focus_set()


mainWindowLaunch()


window.bind("<KeyPress>",keyPress)
window.bind("<Button-1>",mouseClick)

window.mainloop()
