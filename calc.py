# Author: Salvador Murillo
# Project: Python Calculator App
# Description: A python based calculator that uses Tkinter to render
#   GUI interface.

import tkinter as tk
from decimal import Decimal

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("MyCalculator")

        self.displayFrame = tk.Frame(master= self.root)

        # Create label where history is displayed
        self.historyText = tk.StringVar(master= self.root, value= "")
        self.historyDisplay = tk.Label(master= self.displayFrame, textvariable= self.historyText, anchor= tk.E)
        self.historyDisplay.pack(expand= True, fill= "both", pady= 10)

        # Create label where results and input are displayed
        self.entryText = tk.StringVar(master= self.root, value= "0")
        self.entryDisplay = tk.Label(master= self.displayFrame, textvariable= self.entryText, anchor= tk.E)
        self.entryDisplay.pack(expand= True, fill= "both", pady= 10)

        self.displayFrame.pack(anchor= tk.E)

        # Create lock for operation keys, default value is False
        self.keyLock = False

        # Create Frame that contains button keys
        self.keyPad = tk.Frame(master= self.root)
        for i in range(4):
            self.keyPad.columnconfigure(index= i, weight=1)

        # Create numkeys 0 to 9, and insert them into numKeys dictionary
        self.numKeys = {
            str(num): tk.Button(master= self.keyPad, text= str(num), command= lambda num=num: self.insertEntry(str(num))) for num in range(10)
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

        self.keys["BACKSPACE"] = tk.Button(master= self.keyPad, text= u"\u2190", command= self.deleteSingle)
        self.keys["BACKSPACE"].grid(row= 0, rowspan= 2, column= 0, sticky= tk.NSEW)

        self.keys["CE"] = tk.Button(master= self.keyPad, text= "CLR ENTR", command= self.deleteEntry)
        self.keys["CE"].grid(row= 0, rowspan= 2, column= 1, sticky= tk.NSEW)

        self.keys["CH"] = tk.Button(master= self.keyPad, text= "CLR HIST", command= self.deleteHistory)
        self.keys["CH"].grid(row= 0, rowspan= 2, column= 2, sticky= tk.NSEW)

        self.keys["+/-"] = tk.Button(master= self.keyPad, text= "+/-", command= self.switchSign)
        self.keys["+/-"].grid(row= 5, column= 0, sticky= tk.NSEW)

        self.keys["."] = tk.Button(master= self.keyPad, text= ".", command= self.insertDecimal)
        self.keys["."].grid(row= 5, column= 2, sticky= tk.NSEW)

        self.keys["/"] = tk.Button(master= self.keyPad, text= "/", command= lambda: self.insertOperator("/"))
        self.keys["/"].grid(row= 0, column= 3, sticky= tk.NSEW)

        self.keys["*"] = tk.Button(master= self.keyPad, text= "*", command= lambda: self.insertOperator("*"))
        self.keys["*"].grid(row= 1, column= 3, sticky= tk.NSEW)

        self.keys["-"] = tk.Button(master= self.keyPad, text= "-", command= lambda: self.insertOperator("-"))
        self.keys["-"].grid(row= 2, column= 3, sticky= tk.NSEW)

        self.keys["+"] = tk.Button(master= self.keyPad, text= "+", command= lambda: self.insertOperator("+"))
        self.keys["+"].grid(row= 3, column= 3, sticky= tk.NSEW)

        self.keys["="] = tk.Button(master= self.keyPad, text= "=", command= self.equalOp)
        self.keys["="].grid(row= 4, rowspan= 2, column= 3, sticky= tk.NSEW)

        # Pack keyPad frame
        self.keyPad.pack(fill="x")

        self.root.mainloop()

    # Function that changes button background color switching
    def changeButtonColor(self, state):
        items = ["/", "*", "-", "+"]

        if state is True:
            for i in items:
                self.keys[i].configure(bg= "yellow")

        if state is False:
            for i in items:
                self.keys[i].configure(bg= "#F0F0F0")

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
            entry = entry[0 : entry.find(".")]
            self.entryText.set(entry)

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

    # Function that clears history
    def deleteHistory(self):
        self.historyText.set("")

        self.keyLock = False
        self.changeButtonColor(self.keyLock)
    
def main():
    app = calcApp()

if __name__ == "__main__":
    main()