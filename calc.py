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

# Construct key button
class keyButton:
    def __init__(self, master, text, entryInstance, lockInstance):
        self.keyLock = lockInstance
        self.entryInstance = entryInstance
        self.text = text
        self.button = tk.Button(master= master, text= text, command= self.insertEntry)

    # Button entry command for number keys
    def insertEntry(self):
        str = self.entryInstance.get()
        strLen = len(str.replace(",", "")) # Length of numbers minus commas

        # If lock for operation keys is on, replace entry with text
        if self.keyLock.state:
            self.entryInstance.set(self.text)
            self.keyLock.state = False
            return None

        # Prevent appending 0's if current entry string is 0
        if strLen == 1 and str == "0" and self.text == "0":
            return None
        
        # If current entry string is just 0 and text entered is not 0, then replace entry with text
        if strLen == 1 and str == "0" and self.text != "0":
            self.entryInstance.set(self.text)
            return None

        # Appends text entered and handles commas
        if (strLen + 1) % 3 == 1 and (strLen + 1) > 3:
            str = str[0] +"," +str[1:]
            str += self.text

            i = 2 # Skip the first ',' at str[1]
            while str.find(",", i) != -1:
                    i = str.find(",", i)
                    str = str[0 : i] +str[i + 1] +"," +str[i + 2:]
                    i += 2
        else:
            str += self.text

            if (strLen + 1) > 3:
                i = 0
                while str.find(",", i) != -1:
                    i = str.find(",", i)
                    str = str[0 : i] +str[i + 1] +"," +str[i + 2:]
                    i += 2
        
        self.entryInstance.set(str)

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("MyCalculator")

        # Create area where history is displayed
        self.resultNum = None
        self.historyText = tk.StringVar(master= self.root, value= "")
        self.historyDisplay = tk.Label(master= self.root, textvariable= self.historyText)
        self.historyDisplay.pack()

        # Create area where results and input are displayed
        self.entryText = tk.StringVar(master= self.root, value= "0")
        self.entryDisplay = tk.Label(master= self.root, textvariable= self.entryText)
        self.entryDisplay.pack()

        # Create lock for operation keys, default value is False
        self.keyLock = keyLock()

        # Create Frame that contains button keys
        self.keyPad = tk.Frame(master= self.root)
        for i in range(4):
            self.keyPad.columnconfigure(index= i, weight=1)

        # Create numkeys 0 to 9, and insert them into keys dictionary
        self.numKeys = {
            str(num): keyButton(self.keyPad, str(num), self.entryText, self.keyLock) for num in range(10)
        }
        
        # Nested loops that grids numKey buttons within keyPad frame
        key = 9
        for i in range(3):
            offset = 2
            for j in range(3):
                self.numKeys[str(key - offset)].button.grid(row= (i + 2), column= j, sticky=(tk.W + tk.E))
                offset -= 1

            key -= 3

        self.numKeys["0"].button.grid(row= 5, column= 0, columnspan= 2, sticky= (tk.W + tk.E))

        # Create dictionary for keys that are not for numbers
        self.keys = {}

        self.keys["BACKSPACE"] = tk.Button(master= self.keyPad, text= "DEL", command= self.deleteSingle)
        self.keys["BACKSPACE"].grid(row= 0, column= 2, sticky= (tk.W + tk.E))

        self.keys["CLEAR"] = tk.Button(master= self.keyPad, text= "CLEAR", command= self.deleteAll)
        self.keys["CLEAR"].grid(row= 1, column= 2, sticky= (tk.W + tk.E))

        self.keys["."] = tk.Button(master= self.keyPad, text= ".", command= self.insertDecimal)
        self.keys["."].grid(row= 5, column= 2, sticky= (tk.W + tk.E))

        self.keys["/"] = tk.Button(master= self.keyPad, text= "/", command= self.opDivide)
        self.keys["/"].grid(row= 0, column= 3, sticky= (tk.W + tk.E))

        self.keys["*"] = tk.Button(master= self.keyPad, text= "*", command= self.opMultiply)
        self.keys["*"].grid(row= 1, column= 3, sticky= (tk.W + tk.E))

        self.keys["-"] = tk.Button(master= self.keyPad, text= "-", command= self.opSubtract)
        self.keys["-"].grid(row= 2, column= 3, sticky= (tk.W + tk.E))

        self.keys["+"] = tk.Button(master= self.keyPad, text= "+", command= self.opAdd)
        self.keys["+"].grid(row= 3, column= 3, sticky= (tk.W + tk.E))

        self.keys["="] = tk.Button(master= self.keyPad, text= "=", command= self.opEqual)
        self.keys["="].grid(row= 4, rowspan= 2, column= 3, sticky= (tk.NSEW))

        # Pack keyPad frame
        self.keyPad.pack(fill="x")

        self.root.mainloop()

    # Function that takes a integer/decimal and returns it back as a string with commas
    def addCommas(self, num):
        strNum = str(num)
        strLen = len(strNum)

        # If number does not need commas, return
        if strLen <= 3 or strNum.find("E+") != -1:
            return strNum

        # 
        strNum = strNum[::-1]
        i = 0
        numOfCommas = 0
        while i < strLen:
            if ((i + 1) - numOfCommas) % 3 == 1 and (i + 1) > 3:
                strNum = strNum[0 : i] +"," +strNum[i:]
                i += 1
                strLen += 1
                numOfCommas += 1
            
            i += 1

        return strNum[::-1]

    def calculate(self, lNum, rNum):
        if lNum is None:
            return rNum
        
        op = self.historyText.get()[len(self.historyText.get()) - 1]

        if op == "+":
            return lNum + rNum
        elif op == "-":
            return lNum - rNum
        elif op == "*":
            return lNum * rNum
        elif op == "/":
            return lNum / rNum
    
    def deleteSingle(self):
        str = self.entryText.get()
        strLen = len(str.replace(",", ""))
        
        if strLen == 1 and str == "0":
            return None

        if strLen == 1 and str != "0":
            self.entryText.set("0")
            return None

        str = str[:len(str) - 1]

        # If no commas, simply set and leave
        if strLen <= 3:
            self.entryText.set(str)
            return None

        # Update commas by moving them to the left by one index
        i = 0
        while str.find(",", i) != -1:
            i = str.find(",", i)
            str = str[0 : i - 1] +"," +str[i - 1] +str[i + 1:]

            # If ',' is at the start, remove it (ex. 1,231 -> ,123)
            if str[0] == ",":
                str = str[1:]
                i -= 1 # Realing index to match modified 'str', which is off by one

        self.entryText.set(str)

    def deleteAll(self):
        if self.entryText.get() == "0":
            self.resultNum = None
            self.historyText.set("")

        self.entryText.set("0")
        self.keyLock.state = False

    def insertDecimal(self):
        print("Decimal")

    def opDivide(self):
        if self.keyLock.state:
            self.historyText.set(self.historyText.get()[0 : len(self.historyText.get()) - 1] + "/")
            return None
        else:
            self.keyLock.state = True

        entry = self.entryText.get()
        self.resultNum = self.calculate(self.resultNum, Decimal(entry.replace(",", "")))
        self.historyText.set(self.historyText.get() +" " +entry +" /")
        self.entryText.set(self.addCommas(self.resultNum))

    def opMultiply(self):
        if self.keyLock.state:
            self.historyText.set(self.historyText.get()[0 : len(self.historyText.get()) - 1] + "*")
            return None
        else:
            self.keyLock.state = True

        entry = self.entryText.get()
        self.resultNum = self.calculate(self.resultNum, Decimal(entry.replace(",", "")))
        self.historyText.set(self.historyText.get() +" " +entry +" *")
        self.entryText.set(self.addCommas(self.resultNum))

    def opSubtract(self):
        if self.keyLock.state:
            self.historyText.set(self.historyText.get()[0 : len(self.historyText.get()) - 1] + "-")
            return None
        else:
            self.keyLock.state = True

        entry = self.entryText.get()
        self.resultNum = self.calculate(self.resultNum, Decimal(entry.replace(",", "")))
        self.historyText.set(self.historyText.get() +" " +entry +" -")
        self.entryText.set(self.addCommas(self.resultNum))

    def opAdd(self):
        if self.keyLock.state:
            self.historyText.set(self.historyText.get()[0 : len(self.historyText.get()) - 1] + "+")
            return None
        else:
            self.keyLock.state = True

        entry = self.entryText.get()
        self.resultNum = self.calculate(self.resultNum, Decimal(entry.replace(",", "")))
        self.historyText.set(self.historyText.get() +" " +entry +" +")
        self.entryText.set(self.addCommas(self.resultNum))

    def opEqual(self):
        entry = self.entryText.get()
        self.resultNum = self.calculate(self.resultNum, Decimal(entry.replace(",", "")))
        self.historyText.set(self.historyText.get() +" " +entry +" =")
        self.entryText.set(self.addCommas(self.resultNum))
    
def main():
    app = calcApp()

if __name__ == "__main__":
    main()