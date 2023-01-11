# Author: Salvador Murillo
# Project: Python Calculator App
# Description: A python based calculator that uses Tkinter to render
#   GUI interface.

import tkinter as tk
from decimal import Decimal

# Key lock object used to force number input after operation input
# False state -> Unlocked; True state -> Locked
class keyLock:
    def __init__(self):
        self.state = False

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("MyCalculator")

        # Create area where history is displayed
        self.historyText = tk.StringVar(master= self.root, value= "")
        self.historyDisplay = tk.Label(master= self.root, textvariable= self.historyText)
        self.historyDisplay.pack()

        # Create area where results and input are displayed
        self.entryText = tk.StringVar(master= self.root, value= "0")
        self.entryDisplay = tk.Label(master= self.root, textvariable= self.entryText)
        self.entryDisplay.pack()

        # For calculating entry with the recently done operation
        self.recentOp = ""
        self.recentNum = "0"

        # Create lock for operation keys, default value is False
        self.keyLock = keyLock()

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
                self.numKeys[str(key - offset)].grid(row= (i + 2), column= j, sticky=(tk.W + tk.E))
                offset -= 1

            key -= 3

        self.numKeys["0"].grid(row= 5, column= 1, sticky= (tk.W + tk.E))

        # Create dictionary for keys that are not for numbers
        self.keys = {}

        self.keys["BACKSPACE"] = tk.Button(master= self.keyPad, text= "DEL", command= self.deleteSingle)
        self.keys["BACKSPACE"].grid(row= 0, column= 2, sticky= (tk.W + tk.E))

        self.keys["CLEAR"] = tk.Button(master= self.keyPad, text= "CLEAR", command= self.deleteAll)
        self.keys["CLEAR"].grid(row= 1, column= 2, sticky= (tk.W + tk.E))

        self.keys["+/-"] = tk.Button(master= self.keyPad, text= "+/-", command= self.test)
        self.keys["+/-"].grid(row= 5, column= 0, sticky= (tk.W + tk.E))

        self.keys["("] = tk.Button(master= self.keyPad, text= "(", command= self.test)
        self.keys["("].grid(row= 1, column= 0, sticky= (tk.W + tk.E))

        self.keys[")"] = tk.Button(master= self.keyPad, text= ")", command= self.test)
        self.keys[")"].grid(row= 1, column= 1, sticky= (tk.W + tk.E))

        self.keys["."] = tk.Button(master= self.keyPad, text= ".", command= self.test)
        self.keys["."].grid(row= 5, column= 2, sticky= (tk.W + tk.E))

        self.keys["/"] = tk.Button(master= self.keyPad, text= "/", command= lambda: self.insertOperator("/"))
        self.keys["/"].grid(row= 0, column= 3, sticky= (tk.W + tk.E))

        self.keys["*"] = tk.Button(master= self.keyPad, text= "*", command= lambda: self.insertOperator("*"))
        self.keys["*"].grid(row= 1, column= 3, sticky= (tk.W + tk.E))

        self.keys["-"] = tk.Button(master= self.keyPad, text= "-", command= lambda: self.insertOperator("-"))
        self.keys["-"].grid(row= 2, column= 3, sticky= (tk.W + tk.E))

        self.keys["+"] = tk.Button(master= self.keyPad, text= "+", command= lambda: self.insertOperator("+"))
        self.keys["+"].grid(row= 3, column= 3, sticky= (tk.W + tk.E))

        self.keys["="] = tk.Button(master= self.keyPad, text= "=", command= self.equalOp)
        self.keys["="].grid(row= 4, rowspan= 2, column= 3, sticky= (tk.NSEW))

        # Pack keyPad frame
        self.keyPad.pack(fill="x")

        self.root.mainloop()

    def test(self):
        pass

    # Function that changes button background color switching
    def changeButtonColor(self, state):
        items = ["/", "*", "-", "+"]

        if state is True:
            for i in items:
                self.keys[i].configure(bg= "red")

        if state is False:
            for i in items:
                self.keys[i].configure(bg= "#F0F0F0")

    # Function that handles the insertion of numbers being inserted
    def insertEntry(self, entry):
        history = self.historyText.get()

        if len(history) > 0 and history[len(history) - 1] == "=":
            self.historyText.set("")
            self.entryText.set(entry)
            self.recentNum = entry
            self.keyLock.state = False
            self.changeButtonColor(self.keyLock.state)

        elif self.keyLock.state is True:
            self.entryText.set(entry)
            self.recentNum = entry
            self.keyLock.state = False
            self.changeButtonColor(self.keyLock.state)

        else:
            newEntry = self.entryText.get().replace(",", "") +entry
            self.recentNum = "{:,}".format(Decimal(newEntry))
            self.entryText.set("{:,}".format(Decimal(newEntry)))

    # Function that handles the insertion of operators being inserted
    def insertOperator(self, op):
        history = self.historyText.get()
        entry = self.entryText.get()

        if len(history) > 0 and history[len(history) - 1] == "=":
            self.historyText.set(entry +" " +op)
            self.recentOp = op
            self.keyLock.state = True
            self.changeButtonColor(self.keyLock.state)


        elif self.keyLock.state is True:
            self.historyText.set(history[0 : len(history) - 1] +op)
            self.recentOp = op

        else:
            self.keyLock.state = True
            self.changeButtonColor(self.keyLock.state)
            result = eval(history.replace(",", "") +entry.replace(",", ""))
            self.recentOp = op
            self.recentNum = "{:,}".format(result)
            self.historyText.set(history +" " +entry +" " +op)
            self.entryText.set("{:,}".format(result))
    
    # Function that handles the several behaviours of the '=' operation
    def equalOp(self):
        history = self.historyText.get()
        entry = self.entryText.get()

        if self.recentOp == "":
            pass
        
        elif len(history) > 0 and history[len(history) - 1] == "=":
            result = eval(entry.replace(",", "") +self.recentOp +self.recentNum.replace(",", ""))
            self.historyText.set(entry +" " +self.recentOp +" "  +self.recentNum +" =")
            self.entryText.set("{:,}".format(result))

        else:
            result = eval(history.replace(",", "") +entry.replace(",", ""))
            self.historyText.set(history +" " +entry +" =")
            self.entryText.set("{:,}".format(result))

    # Function that deletes 1-character from the entry text
    def deleteSingle(self):
        entry = self.entryText.get().replace(",", "")
        
        if len(entry) == 1 and entry == "0":
            return None

        if len(entry) == 1 and entry != "0":
            self.entryText.set("0")
            return None

        entry = "{:,}".format(Decimal(entry[:len(entry) - 1])) # Bug with negatives
        self.recentNum = entry
        self.entryText.set(entry)

    # Function that handles clearing of entry and history
    def deleteAll(self): # FIX! maybe add other button
        entry = self.entryText.get()
        if entry == "0":
            self.historyText.set("")

        self.entryText.set("0")
        self.keyLock.state = False
        self.changeButtonColor(self.keyLock.state)
    
def main():
    app = calcApp()

if __name__ == "__main__":
    main()