# Basic Calculator using Python and Tkinter

## Description

A basic calculator written in Python. The graphical interface is built with Tkinter. The calculator supports multiplication, division, addition, and subtration operations. Decimals, and negative numbers are also supported (decimals still need work as some results are inaccurate). Input from keyboard is supported; keyboard inputs will correspond to buttons of the calculator app. Other features that manipulate the entry and history labels are also provided (clear all fields, clear entry field, and backspace).

The calculator consists of a frame of buttons (the keypad), and a frame that displays the user's entry and the operations the user added. The display frame consists of the entry label (where the user inputs numbers), and the history label (where the past operations are displayed). Python's eval() function is used to evaluate the expressions the user enters.

## Bugs/Needed Features

- When evaluating expressions with decimals, some results will be inaccurate.
- Entry and history fields will run off the text if too many characters are entered. A possible fix is to change the font size when a certain amount of characters are entered. Another possible fix is to keep the run off text, but provide a slider that will slide across the entered text/expression.