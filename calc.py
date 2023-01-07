# Author: Salvador Murillo
# Project: Python Calculator App
# Description: A python based calculator that uses Tkinter to render
#   GUI interface.

import tkinter as tk

# Construct key button
class keyButton:
    def __init__(self, master, text, instance):
        self.entryInstance = instance
        self.text = text
        self.button = tk.Button(master= master, text= text, command= self.insertEntry)

    # Button entry command for number keys
    def insertEntry(self):
        str = self.entryInstance.get()
        strLen = len(str.replace(",", "")) # Length of numbers minus commas

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
                    str = str[:i] +str[i + 1] +"," +str[i + 2:]
                    i = str.find(",", i) + 1
        else:
            str += self.text

            if (strLen + 1) > 3:
                i = 0
                while str.find(",", i) != -1:
                    i = str.find(",", i)
                    str = str[:i] +str[i + 1] +"," +str[i + 2:]
                    i = str.find(",", i) + 1
        
        self.entryInstance.set(str)

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("MyCalculator")

        # Create area where results and input are displayed
        self.entryText = tk.StringVar(self.root, "0")
        self.display = tk.Label(self.root, textvariable= self.entryText)
        self.display.pack()

        # Create Frame that contains button keys
        self.keyPad = tk.Frame(master=  self.root)
        for i in range(4):
            self.keyPad.columnconfigure(i, weight=1)

        # Create numkeys 0 to 9, and insert them into keys dictionary
        self.numKeys = {
            str(num): keyButton(self.keyPad, str(num), self.entryText) for num in range(10)
        }
        
        # Nested loops that grids numKey buttons within keyPad frame
        key = 9
        for i in range(3):
            offset = 2
            for j in range(3):
                self.numKeys[str(key - offset)].button.grid(row= (i + 1), column= j, sticky=(tk.W + tk.E))
                offset -= 1

            key -= 3

        self.numKeys["0"].button.grid(row= 4, column= 0, columnspan= 2, sticky= (tk.W + tk.E))

        self.keyPad.pack(fill="x")

        self.root.mainloop()
            
    
def main():
    app = calcApp()

if __name__ == "__main__":
    main()