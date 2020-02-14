import tkinter as tk
from tkinter import scrolledtext
import re
from pynput.keyboard import Listener, Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import winsound

#button1 command

def callback():
    #set up array
    #arrange the string into array(1D) to be parsed then put in 2D array
    temp = txt.get("1.0", "end-1c")
    temp = temp.replace("_", "")
    temp = temp.replace("-", "")

    arrangeA = temp.split()
    #ordering the 2D array
    orderA =[]
    reading = False
    truckLoad = False
    for item in arrangeA:
        
        if item.lower() == "deductions/earnings":
            truckLoad = True
        #need a false statement
        
        if item == "Deduction" and truckLoad == True:
            reading = True
        if item == "Reimbursement" and truckLoad == True:
            reading = True
        if item == "Earning" and truckLoad == True:
            reading = True
        if item.count("$")>0 and reading == True:
            orderA.append(item)
            reading = False
        if reading == True and truckLoad == True:
            orderA.append(item)

    reading = False
    truckLoad = False
    runningTotal = 0
    for item in arrangeA:
        
        if item == "DEDUCTIONS":
            truckLoad = True
        if item.count("$")>0 and truckLoad == True:
            if float(item.replace("$", "").replace(",", "")) == runningTotal:
                runningTotal = 0
                truckLoad = False
                reading = False






        if reading == True and truckLoad == True:
            if item.count("$")>0:
                runningTotal = round(runningTotal + float(item.replace("$", "").replace(",", "")), 2)
            orderA.append(item)
        if item == "Rate" and truckLoad == True:   
            reading = True
        
    typeO = []
    description = []
    cost = []
    typeAdded = False
    tempString = ""
    for item in orderA:
        if item == "Deduction" or item == "Reimbursement" or item == "Earning":
           typeO.append(item)
           typeAdded = True
        elif typeAdded == False:
            typeO.append("")
            typeAdded = True

        if item.count("$")>0 and typeAdded == True:
            cost.append(abs(round(float(item.replace("$", "").replace(",", "").replace("-", "")), 2)))
            typeAdded = False
            description.append(tempString)
            tempString = ""
            
        elif typeAdded == True:
            
            tempString = tempString + " " + item

            
    file = open("codes.txt", "r")
    fileContent = []
    for line in file:
        fileContent.append(line)
    file.close()
    i = 0
    
    while i < len(description):
        if typeO[i] == "Deduction" or typeO[i] == "" or typeO[i] == "Earning":
            for line in fileContent:
                if description[i].find(re.sub("[\d-]", "", "ATBS/FHUT").strip()) > 0:
                    description[i] = 36
                    cost[i] = float(cost[i] - 12)
                    description.insert(i+1, 67)
                    cost.insert(i+1, 12)
                    i = i + 1
                if description[i] == 77 and [2, 2.5, 11, 11.5, 12].count(float(cost[i])) > 0:
                    description[i] = 66
                if description[i].find(re.sub("[\d-]", "", line).strip()) > 0:


                
                    description[i] = re.sub("[^0-9.]", "", line)
        if typeO[i] == "Reimbursement":
            x = 0
            while x < len(typeO):
                if abs(cost[x]) == abs(cost[i]) and x <= i:
                    description[i] = description[x]
                    cost[i] = -abs(cost[i])
                    x = len(typeO)
                    
                else:
                    description[i] = 107
                
                x = x + 1
            if description[i] == 107:
                cost[i] = abs(cost[i])
        if cost[i] == 0:
            cost.pop(i)
            description.pop(i)
            typeO.pop(i)
        i = i + 1

    time.sleep(5)
    i = 0
    
    mouse = MouseController()

    file = open("settings.txt", "r")
    x1 = int (re.sub("[^0-9.]", "", file.readline()))
    y1 = int (re.sub("[^0-9.]", "", file.readline()))
    jump1 = int (re.sub("[^0-9.]", "", file.readline()))
    jump2 = int (re.sub("[^0-9.]", "", file.readline()))
    x2 = int (re.sub("[^0-9.]", "", file.readline()))
    y2 = int (re.sub("[^0-9.]", "", file.readline()))
    time1 = float (re.sub("[^0-9.]", "", file.readline()))
    time2 = float (re.sub("[^0-9.]", "", file.readline()))
    left = int (re.sub("[^0-9.]", "", file.readline()))

    
    keyboard = KeyboardController()         
    while i < len(typeO):
        keyBoardEnter(description[i], cost[i], time1, time2)
        i = i + 1


    winsound.Beep(2000, 400)
    
    
def keyBoardEnter(description, cost, time1, time2):
    keyboard = KeyboardController()
     
      
    #TYPE IN CODE, MOVE TO $AMOUNT
    keyboard.type(str(description))
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(time1)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    
    
    #TYPE IN $ AMOUNT, MOVE TO BUTTON
    keyboard.type(str(cost))
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(time1)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    

    # CLICK BUTTON, MOVE TO RESET
    keyboard.press(Key.enter)
    time.sleep(0.3)
    keyboard.release(Key.enter)
    time.sleep(0.4)
    if int(description) == 68:
        keyboard.press(Key.enter)
        time.sleep(0.3)
        keyboard.release(Key.enter)
    time.sleep(time2)
        
        



def mouseEnter():

        y = y1
        if [10, 21, 28, 29, 31, 36, 37, 49, 51, 52, 54, 55, 60, 65, 68, 69, 74, 78, 79, 106, 108, 109].count(int(description[i])) > 0:
            y = jump1
        elif [38, 73, 77].count(int(description[i])) > 0:
            y = jump2

        print(y)




        
        #TYPE IN CODE, MOVE TO $AMOUNT
        #mouse.move(x1,y1)
        mouse.click(Button.left, 1)
        keyboard.type(str(description[i]))
        mouse.move(left,0)
        time.sleep(time1)
        mouse.click(Button.left, 1)
        mouse.move(-left,0)
        mouse.move(x1,y)


        
        #TYPE IN $ AMOUNT, MOVE TO BUTTON
        time.sleep(time1)
        mouse.click(Button.left, 1)
        #keyboard.press(Key.tab)
        #keyboard.release(Key.tab)
        #time.sleep(0.35)
        #keyboard.press(Key.tab)
        #time.sleep(0.35)
        #keyboard.release(Key.tab)
        #time.sleep(0.35)
        keyboard.type(str(cost[i]))
        mouse.move(left,0)
        time.sleep(time1)
        mouse.click(Button.left, 1)
        mouse.move(-left,0)
        mouse.move(x2,y2)


        # CLICK BUTTON, MOVE TO RESET
        time.sleep(time1)
        mouse.click(Button.left, 1)
        mouse.move(-(x1+x2),-(y + y2))
        #keyboard.press(Key.tab)
        #time.sleep(0.35)
        #keyboard.release(Key.tab)
        #time.sleep(0.35)
        #keyboard.press(Key.tab)
        #time.sleep(0.35)
        #keyboard.release(Key.tab)
        #time.sleep(0.35)
        #keyboard.press(Key.enter)
        #time.sleep(0.35)
        #keyboard.release(Key.enter)
        
        time.sleep(time2)
        





  
#set up window
window = tk.Tk()
window.title("Typer")
window.geometry("800x800")
lbl = tk.Label(window, text=" enter instructions here")
lbl.grid(column=1,row=0)
mouse = MouseController()
#button1
btn = tk.Button(window, text="click me", command=callback)
btn.grid(column=1, row=1)

#font
txt = scrolledtext.ScrolledText(window,width=40, height=20)
txt.config(font=("courier", 15, "normal"))
txt.grid(column=1, row=2)
window.mainloop()


