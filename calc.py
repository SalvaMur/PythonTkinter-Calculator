# Author: Salvador Murillo
# Project: Python Calculator App
# Description: A python based calculator that uses Tkinter to render
#   GUI interface.

import tkinter as tk
from decimal import Decimal

# Font styles
LARGE_FONT = "Arial 40 bold"
SMALL_FONT = "Arial 20"
BUTTON_FONT = "Arial 14"

# Colors
HISTORY_TEXT_COLOR = "gray"
OPERATOR_COLOR = "orange"
ALT_OPERATOR_COLOR = "yellow"
EQUAL_BUTTON_COLOR = "light blue"

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("322x502")
        self.root.resizable(width= False, height= False)
        self.root.title("Basic Calculator")
        self.root.iconbitmap("BasicCalculator.ico")

        # Frame that contains all widgets.
        self.appFrame = tk.Frame(master= self.root)
        #self.appFrame.configure(bg= "red", borderwidth= 2) # Uncomment to see frame

        # Frame that contains the display labels
        self.displayFrame = tk.Frame(master= self.appFrame)
        #self.displayFrame.configure(bg= "blue", borderwidth= 2) # Uncomment to see frame

        # Create label where history is displayed
        self.historyText = tk.StringVar(master= self.root, value= "")
        self.historyDisplay = tk.Label(master= self.displayFrame, 
            textvariable= self.historyText, anchor= tk.E, font= SMALL_FONT,
            padx= 10, fg= HISTORY_TEXT_COLOR, 
        )
        self.historyDisplay.pack(expand= True, fill= "both")

        # Create label where results and input are displayed
        self.entryText = tk.StringVar(master= self.root, value= "0")
        self.entryDisplay = tk.Label(master= self.displayFrame, 
            textvariable= self.entryText, anchor= tk.E, font= LARGE_FONT,
            padx= 10
        )
        self.entryDisplay.pack(expand= True, fill= "both")

        self.displayFrame.pack(expand= True, fill= "both")

        # Create lock for operation keys, default value is False
        self.keyLock = False

        # Create Frame that contains button keys
        self.keyPad = tk.Frame(master= self.appFrame)
        #self.keyPad.configure(bg= "yellow", borderwidth= 2) # Uncomment to see frame

        for i in range(4):
            self.keyPad.columnconfigure(index= i, weight= 1)

        for i in range(6):
            self.keyPad.rowconfigure(index= i, weight= 1)

        # Create numkeys 0 to 9, and insert them into numKeys dictionary
        self.numKeys = {
            str(num): tk.Button(master= self.keyPad, text= str(num), 
                command= lambda num=num: self.insertEntry(str(num)),
                font= BUTTON_FONT
            ) for num in range(10)
        }
        
        # Nested loops that grids numKey buttons within keyPad frame
        key = 9
        for i in range(3):
            offset = 2
            for j in range(3):
                self.numKeys[str(key - offset)].grid(row= (i + 2), column= j, sticky=tk.NSEW)
                offset -= 1

            key -= 3

        self.numKeys["0"].grid(row= 5, column= 1, sticky= tk.NSEW)

        # Create dictionary for keys that are not for numbers
        self.keys = {}

        self.keys["BACKSPACE"] = tk.Button(master= self.keyPad, text= u"\u2190", 
            command= self.deleteSingle, font= BUTTON_FONT
        )
        self.keys["BACKSPACE"].grid(row= 0, rowspan= 2, column= 0, sticky= tk.NSEW)

        self.keys["CE"] = tk.Button(master= self.keyPad, text= "CE", 
            command= self.deleteEntry, font= BUTTON_FONT
        )
        self.keys["CE"].grid(row= 0, rowspan= 2, column= 1, sticky= tk.NSEW)

        self.keys["C"] = tk.Button(master= self.keyPad, text= "C", 
            command= self.deleteAll, font= BUTTON_FONT
        )
        self.keys["C"].grid(row= 0, rowspan= 2, column= 2, sticky= tk.NSEW)

        self.keys["+/-"] = tk.Button(master= self.keyPad, text= "+/-", 
            command= self.switchSign, font= BUTTON_FONT
        )
        self.keys["+/-"].grid(row= 5, column= 0, sticky= tk.NSEW)

        self.keys["."] = tk.Button(master= self.keyPad, text= ".", 
            command= self.insertDecimal, font= BUTTON_FONT
        )
        self.keys["."].grid(row= 5, column= 2, sticky= tk.NSEW)

        self.keys["/"] = tk.Button(master= self.keyPad, text= "/", 
            command= lambda: self.insertOperator("/"), font= BUTTON_FONT,
            bg= OPERATOR_COLOR
        )
        self.keys["/"].grid(row= 0, column= 3, sticky= tk.NSEW)

        self.keys["*"] = tk.Button(master= self.keyPad, text= "*", 
            command= lambda: self.insertOperator("*"), font= BUTTON_FONT,
            bg= OPERATOR_COLOR
        )
        self.keys["*"].grid(row= 1, column= 3, sticky= tk.NSEW)

        self.keys["-"] = tk.Button(master= self.keyPad, text= "-", 
            command= lambda: self.insertOperator("-"), font= BUTTON_FONT,
            bg= OPERATOR_COLOR
        )
        self.keys["-"].grid(row= 2, column= 3, sticky= tk.NSEW)

        self.keys["+"] = tk.Button(master= self.keyPad, text= "+", 
            command= lambda: self.insertOperator("+"), font= BUTTON_FONT,
            bg= OPERATOR_COLOR
        )
        self.keys["+"].grid(row= 3, column= 3, sticky= tk.NSEW)

        self.keys["="] = tk.Button(master= self.keyPad, text= "=", 
            command= self.equalOp, font= BUTTON_FONT, bg= EQUAL_BUTTON_COLOR
        )
        self.keys["="].grid(row= 4, rowspan= 2, column= 3, sticky= tk.NSEW)

        # Pack keyPad frame
        self.keyPad.pack(expand= True, fill= "both")

        self.appFrame.pack(expand= True, fill= "both")

        self.root.bind("<Key>", self.keyboardInput)

        self.root.mainloop()

    # Function that handles keyboard input
    def keyboardInput(self, event):
        keyOp = ['/', '*', '-', '+']
        numKeys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        if event.keysym == "Return":
            self.equalOp()

        elif event.char in keyOp:
            self.insertOperator(event.char)
        
        elif event.char in numKeys:
            self.insertEntry(event.char)

        elif event.keysym == "period":
            self.insertDecimal()

        elif event.keysym == "BackSpace":
            self.deleteSingle()

        elif event.state == 262153 and event.keysym == "Delete":
            self.deleteAll()

        elif event.state == 262152 and event.keysym == "Delete":
            self.deleteEntry()

    # Function that changes button background color switching
    def changeButtonColor(self, state):
        items = ["/", "*", "-", "+"]

        if state is True:
            for i in items:
                self.keys[i].configure(bg= ALT_OPERATOR_COLOR)

        if state is False:
            for i in items:
                self.keys[i].configure(bg= OPERATOR_COLOR)

    # Function that handles the insertion of numbers being inserted
    def insertEntry(self, entry):
        history = self.historyText.get()

        if history.find("=") != -1:
            self.historyText.set("")
            self.entryText.set(entry)

            self.keyLock = False
            self.changeButtonColor(self.keyLock)

        elif self.keyLock is True:
            self.entryText.set(entry)

            self.keyLock = False
            self.changeButtonColor(self.keyLock)

        else:
            newEntry = self.entryText.get().replace(",", "") +entry
            self.entryText.set("{:,}".format(Decimal(newEntry)))

    # Function that handles the insertion of operators being inserted
    def insertOperator(self, op):
        history = self.historyText.get()
        entry = self.entryText.get()

        if entry == "ERROR":
            pass

        elif history.find("=") != -1:
            self.historyText.set(entry +" " +op)

            self.keyLock = True
            self.changeButtonColor(self.keyLock)

        elif self.keyLock is True:
            self.historyText.set(history[0 : len(history) - 1] +op)

        else:
            self.keyLock = True
            self.changeButtonColor(self.keyLock)

            try:
                result = eval(history.replace(",", "") +entry.replace(",", ""))
                self.historyText.set(history +" " +entry +" " +op)
                self.entryText.set("{:,}".format(result))
            except:
                self.historyText.set("")
                self.entryText.set("ERROR")
    
    # Function that handles the several behaviours of the '=' operation
    def equalOp(self):
        history = self.historyText.get()
        entry = self.entryText.get()

        if history.find("=") != -1:
            self.historyText.set("")
            
            self.keyLock = False
            self.changeButtonColor(self.keyLock)

        else:
            try:
                result = eval(history.replace(",", "") +entry.replace(",", ""))
                self.historyText.set(history +" " +entry +" =")
                self.entryText.set("{:,}".format(result))
            except:
                self.keyLock = True
                self.changeButtonColor(self.keyLock)

                self.historyText.set("")
                self.entryText.set("ERROR")

    # Toggle entry between positive or negative
    def switchSign(self):
        entry = self.entryText.get()

        if entry == "0":
            pass

        elif entry.find("-") == 0:
            self.entryText.set(entry[1:])

        else:
            self.entryText.set("-" +entry)

    # Toggle between having a decimal or not for entry
    def insertDecimal(self):
        entry = self.entryText.get()

        if entry.find(".") == -1:
            entry = entry +"."
            self.entryText.set(entry)
        else:
            pass

    # Function that deletes 1-character from the entry text
    def deleteSingle(self):
        entry = self.entryText.get().replace(",", "")
        
        if len(entry) == 1 and entry == "0":
            pass

        elif len(entry) == 1 and entry != "0":
            self.entryText.set("0")
        
        elif len(entry) == 2 and entry.find("-") == 0:
            self.entryText.set("0")

        else:
            entry = "{:,}".format(Decimal(entry[0 : len(entry) - 1]))
            self.entryText.set(entry)

    # Function that clears entry
    def deleteEntry(self):
        self.entryText.set("0")

        self.keyLock = False
        self.changeButtonColor(self.keyLock)

    # Function that clears history label and entry label
    def deleteAll(self):
        self.historyText.set("")
        self.entryText.set("0")

        self.keyLock = False
        self.changeButtonColor(self.keyLock)
    
def main():
    app = calcApp()

if __name__ == "__main__":
    main()