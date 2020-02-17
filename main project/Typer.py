import tkinter as tk
from tkinter import scrolledtext
import re
from pynput.keyboard import Listener, Key, Controller as KeyboardController
import time
import winsound






def buttonClick(txt):
    arrangeA = parse(txt)
    dataEntries = [[],[],[]]
    
    #Roadrunner
    if arrangeA.count("Roadrunner") > 0:
        dataEntries = roadrunner(arrangeA)
    elif arrangeA.count("KAG"):        
        dataEntries = kenan(arrangeA)
    elif arrangeA.count("Henderson"):
        dataEntries = henderson(arrangeA)
    keyBoardEnter(dataEntries)


    
def parse(temp):
    temp = temp.replace("_", "")
    temp = temp.replace("-", "")
    arrangeA = temp.split()
    return arrangeA

def henderson(arrangeA):
    dataEntries = hendersonReads(arrangeA)
    dataEntries = hendersonCodes(dataEntries)
    dataEntries = hendersonExcept(dataEntries)
    return dataEntries


def hendersonReads(arrangeA):

    orderA = []
    dataEntries = [[],[],[]]

    reading = False
    truckLoad = False
    for item in arrangeA:

        if str(re.search("[A-Za-z]", item)) != "None" and str(re.search("[\d]", item)) != "None":
            item = re.sub("[\d]", "",item.replace("$", "").replace(".", ""))
            

        #when to read items
        if item.lower() == "deductions/earnings":
            truckLoad = True
            reading = False
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

    #set reading to False
    reading = False
    truckLoad = False

    #last part of settlement
    runningTotal = 0
    for item in arrangeA:

        #print("Item: " + item + " Letters: " + str(str(re.search("[A-Za-z]", item)) != "None") + " Numbers: " + str(str(re.search("[\d]", item)) != "None"))

        
        
        if item == "DEDUCTIONS": 
            truckLoad = True
            reading = False
        if str(re.search("[A-Za-z]", item)) != "None" and str(re.search("[\d]", item)) != "None":
            item = re.sub("[\d]", "",item.replace("$", "").replace(".", ""))
            print(item)
            
        if item.count("$")>0 and truckLoad == True:
            if float(item.replace("$", "").replace(",", "")) == runningTotal:
                runningTotal = 0
                truckLoad = False
                reading = False
            if item == "Owner":
                reading = False
            if item == "Pay":
                reading = True

        if item == "EARNINGS":
            truckLoad = True
            
        if item.count("$")>0 and truckLoad == True:
            if float(item.replace("$", "").replace(",", "")) == runningTotal:
                runningTotal = 0
                truckLoad = False
                reading = False
            

        if item == "REIMBURSEMENTS":
            truckLoad = True
            runningTotal = 0
        if item.count("$")>0 and truckLoad == True:
            if float(item.replace("$", "").replace(",", "")) == runningTotal:
                runningTotal = 0
                truckLoad = False
                reading = False
            if item == "Owner":
                reading = False
            if item == "Pay":
                reading = True

        if reading == True and truckLoad == True:
            if item.count("$")>0:
                runningTotal = round(runningTotal + float(item.replace("$", "").replace(",", "")), 2)
            orderA.append(item)
        if item == "Rate" and truckLoad == True:   
            reading = True

        #need to do same for erarnings and reimbusements, and pay summary

        
    # dataEntries[[],[],[]]
    # dataEntries[0] is the type of transaction
    # dataEntries[1] is the discription to be turned into acct. code
    # dataEntries[2] is the cost of the transaction
    typeAdded = False
    tempString = ""
    for item in orderA:
        if item == "Deduction" or item == "Reimbursement" or item == "Earning":
           dataEntries[0].append(item)
           typeAdded = True
        elif typeAdded == False:
            dataEntries[0].append("")
            typeAdded = True

        if item.count("$")>0 and typeAdded == True:
            dataEntries[2].append(abs(round(float(item.replace("$", "").replace(",", "").replace("-", "")), 2)))
            typeAdded = False
            dataEntries[1].append(tempString)
            tempString = ""
            
        elif typeAdded == True:
            
            tempString = tempString + " " + item


    i = 0
    while i < len(dataEntries[2]):
        if dataEntries[2][i] == 0:
            dataEntries[2].pop(i)
            dataEntries[1].pop(i)
            dataEntries[0].pop(i)
        i = i + 1
    









    return dataEntries

def hendersonCodes(dataEntries):

    file = open("Henderson Codes.txt", "r")
    fileContent = []
    for line in file:
        fileContent.append(line)
    file.close()
    i = 0
    while i < len(dataEntries[1]):
        
        for x in fileContent:

            if dataEntries[1][i].find(re.sub("[\d-]", "", "ATBS/FHUT").strip()) > 0:
                    dataEntries[1][i] = 36
                    dataEntries[2][i] = float(dataEntries[2][i] - 12)
                    dataEntries[1].insert(i+1, 67)
                    dataEntries[2].insert(i+1, 12)
                    dataEntries[0].insert(i+1, "")
                    if i < len(dataEntries[1]) - 2:
                        i = i + 2
                     


            

            #switch discription to codes
            #if dataEntries[0][i] == "Deduction" or dataEntries[0][i] == "" or dataEntries[0][i] == "Earning":
                #if dataEntries[1][i].find(re.sub("[\d-]", "", x).strip()) > 0:
                    dataEntries[1][i] = re.sub("[^0-9.]", "", x)

            

            #switch discription to codes
            #str(re.sub("[\d-]", "", dataEntries[1][i])))
                
            why = str(re.sub("\s", "", re.sub("[\d-]", "", x)))
            OMG = re.sub("\s", "", str(re.sub("[\d-]", "", dataEntries[1][i])))
            #print(str(OMG.find(why)) + " | " + why + " | " + OMG)
            if OMG.find(why) >= 0:
                dataEntries[1][i] = re.sub("[^0-9.]", "", x)

            


            
        # reimbusements to change code at roadrunnerExcept()     
        if dataEntries[0][i] == "Reimbursement":
            dataEntries[1][i] = 107
            dataEntries[2][i] = abs(dataEntries[2][i])

        
        i = i + 1


    return dataEntries

def hendersonExcept(dataEntries):
    i = 0
    while i < len(dataEntries[2]):
        if dataEntries[1][i] == "969":
            dataEntries[1][i] = "69"
            dataEntries[2][i] = -abs(dataEntries[2][i])

        if dataEntries[1][i] == "963":
            dataEntries[1][i] = "63"
            dataEntries[2][i] = -abs(dataEntries[2][i])

        if dataEntries[1][i] == "9105":
            dataEntries[1][i] = "105"
            dataEntries[2][i] = -abs(dataEntries[2][i])

        i = i + 1
    return dataEntries

def kenan(arrangeA):
    dataEntries = kenanReads(arrangeA)
    dataEntries = kenanCodes(dataEntries)
    dataEntries = kenanExcept(dataEntries)
    

    return dataEntries



def kenanReads(arrangeA):
    milesA = []
    orderA = []
    dataEntries = [[],[],[]]

    reading = True
    truckLoad = False



    #pick up miles to milesA[]
    i = 0
    while i < len(arrangeA):
        
        if i < len(arrangeA)-7 and (arrangeA[i + 3] + arrangeA[i + 4] + arrangeA[i + 5] + arrangeA[i + 6] + arrangeA[i + 7] == "Totaltrippaythisperiod:"):
            reading = False
        if arrangeA[i] == "Gallons" and reading == True:
            milesA.append(arrangeA[i + 9])
        if arrangeA[i] == "Amount:" and reading == True and arrangeA[i + 10].count("/")== 0 and arrangeA[i + 10].count(":") == 0:
            milesA.append(arrangeA[i + 10])
        i = i + 1





    reading = False
    truckLoad = False
    i = 0
    while i < len(arrangeA):


        #when to read earnings
        if arrangeA[i] == "Gallons":
            truckLoad = True
        if arrangeA[i] == "Amount" and truckLoad == True:
            reading = True
        if arrangeA[i] == "Total" and truckLoad == True:
            reading = False
        if i < len(arrangeA)-7 and (arrangeA[i + 3] + arrangeA[i + 4] + arrangeA[i + 5] + arrangeA[i + 6] + arrangeA[i + 7] == "Totaltrippaythisperiod:"):
            truckLoad = False
        if reading == True and truckLoad == True and arrangeA[i] != "Amount" and arrangeA[i] != "Total":
            orderA.append(arrangeA[i])

        i = i + 1
    
    #set reading to False
    reading = False
    truckLoad = False

    i = 0
    while i < len(arrangeA):

        if i < len(arrangeA)-1  and (arrangeA[i] + arrangeA[i + 1] == "Misc.Deductions:"):
            truckLoad = True
        if arrangeA[i] == "YTD":
            reading = True
        if i < len(arrangeA)-1  and (arrangeA[i] + arrangeA[i + 1] == "TotalAmount:"):
            reading = False
        if reading == True and truckLoad == True and arrangeA[i] != "Amount" and arrangeA[i] != "Total":
            orderA.append(arrangeA[i])
        i = i + 1
    


    for item in milesA:
        dataEntries[1].append("miles")
        dataEntries[2].append(int(item.replace(",", "")))
    i = 0
    while i < len(orderA):
        


        if i < len(orderA)-3 and orderA[i].replace('.', "", 1).replace(',', "", 1).replace("(", "").replace(")", "").replace("$", "").isdigit() == False and orderA[i + 1].replace('.', "", 1).replace(',', "", 1).replace("(", "").replace(")", "").replace("$", "").isdigit() == True:
            dataEntries[2].append(orderA[i + 3])
        
        if orderA[i].replace('.', "", 1).replace("$", "").replace(',', "", 1).replace("(", "").replace(")", "").isdigit() == False and orderA[i - 1].replace('.', "", 1).replace(',', "", 1).replace("$", "").replace("(", "").replace(")", "").isdigit() == False:
            orderA[i - 1] = orderA[i - 1] + " " + orderA[i]
            orderA.pop(i)
            i = i - 1

        

        i = i + 1
    i = 0
    while i < len(orderA):


        if  orderA[i].replace('.', "", 1).replace(',', "", 1).replace("$", "").replace("(", "").replace(")", "").isdigit() == True:
            orderA.pop(i)
            i = i - 1




        i = i + 1
    dataEntries[1] =  dataEntries[1] + orderA
    

    return dataEntries


def kenanCodes(dataEntries):
    file = open("Kenan Codes.txt", "r")
    fileContent = []
    for line in file:
        fileContent.append(re.sub("\s", "", line))
    file.close()
    i = 0
    # modifying Data entries array into a standard format
    while i < len(dataEntries[2]):
        if str(dataEntries[2][i]).isdigit() == False and str(dataEntries[2][i]).count("$")>0:
            dataEntries[0].append("Earning")
        else:
            dataEntries[0].append("Deduction")

        if str(dataEntries[2][i]).isdigit() == False:
            dataEntries[2][i] = str(dataEntries[2][i].replace(',', "").replace("$", "").replace("(", "-").replace(")", ""))
        i = i + 1


    #knock off those 0's
    i = 0
    while i < len(dataEntries[2]):
        if dataEntries[2][i] == "0.00":
            dataEntries[2].pop(i)
            dataEntries[1].pop(i)
            dataEntries[0].pop(i)
        i = i + 1

    i = 0
    while i < len(dataEntries[1]):
    
        for x in fileContent:

            #switch discription to codes
            #str(re.sub("[\d-]", "", dataEntries[1][i])))
            why = str(re.sub("[\d-]", "", x)).replace(" ", "")
            OMG = re.sub("\s", "", str(re.sub("[\d-]", "", dataEntries[1][i])))
            if OMG.find(why) >= 0:
                dataEntries[1][i] = re.sub("[^0-9.]", "", x)


        i = i + 1
    return dataEntries

def kenanExcept(dataEntries):



    return dataEntries   

def roadrunner(arrangeA):
    dataEntries = roadrunnerReads(arrangeA)
    dataEntries = roadrunnerCodes(dataEntries)
    dataEntries = roadrunnerExcept(dataEntries)

    return dataEntries
    
def roadrunnerReads(arrangeA):
    orderA = []
    dataEntries = [[],[],[]]

    reading = False
    truckLoad = False
    for item in arrangeA:



        #when to read items
        if item.lower() == "deductions/earnings":
            truckLoad = True
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

    #set reading to False
    reading = False
    truckLoad = False

    #last part of settlement
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


        #need to do same for erarnings and reimbusements, and pay summary

        
    # dataEntries[[],[],[]]
    # dataEntries[0] is the type of transaction
    # dataEntries[1] is the discription to be turned into acct. code
    # dataEntries[2] is the cost of the transaction
    typeAdded = False
    tempString = ""
    for item in orderA:
        if item == "Deduction" or item == "Reimbursement" or item == "Earning":
           dataEntries[0].append(item)
           typeAdded = True
        elif typeAdded == False:
            dataEntries[0].append("")
            typeAdded = True

        if item.count("$")>0 and typeAdded == True:
            dataEntries[2].append(abs(round(float(item.replace("$", "").replace(",", "").replace("-", "")), 2)))
            typeAdded = False
            dataEntries[1].append(tempString)
            tempString = ""
            
        elif typeAdded == True:
            
            tempString = tempString + " " + item


    i = 0
    while i < len(dataEntries[2]):
        if dataEntries[2][i] == 0:
            dataEntries[2].pop(i)
            dataEntries[1].pop(i)
            dataEntries[0].pop(i)
        i = i + 1
    return dataEntries


def roadrunnerCodes(dataEntries):

    file = open("Roadrunner Codes.txt", "r")
    fileContent = []
    for line in file:
        fileContent.append(line)
    file.close()
    i = 0
    while i < len(dataEntries[0]):
        
        for x in fileContent:

            if dataEntries[1][i].find(re.sub("[\d-]", "", "ATBS/FHUT").strip()) > 0:
                    dataEntries[1][i] = 36
                    dataEntries[2][i] = float(dataEntries[2][i] - 12)
                    dataEntries[1].insert(i+1, 67)
                    dataEntries[2].insert(i+1, 12)
                    dataEntries[0].insert(i+1, "")
                    i = i + 2


            

            #switch discription to codes
            if dataEntries[0][i] == "Deduction" or dataEntries[0][i] == "" or dataEntries[0][i] == "Earning":
                if dataEntries[1][i].find(re.sub("[\d-]", "", x).strip()) > 0:
                    dataEntries[1][i] = re.sub("[^0-9.]", "", x)

        # reimbusements to change code at roadrunnerExcept()     
        if dataEntries[0][i] == "Reimbursement":
            dataEntries[1][i] = 107
            dataEntries[2][i] = abs(dataEntries[2][i])

        
        i = i + 1

    return dataEntries



def roadrunnerExcept(dataEntries):
    i = 0
    while i < len(dataEntries[1]):
        if dataEntries[0][i] == "Reimbursement":
            x = 0
           

            
            while x < len(dataEntries[0]):
                if abs(dataEntries[2][x]) == abs(dataEntries[2][i]):
                    dataEntries[1][i] = dataEntries[1][x]
                    dataEntries[2][i] = -abs(dataEntries[2][i])
                if dataEntries[1][i] == 107:
                    dataEntries[2][i] = abs(dataEntries[2][i])  
                
              
                x = x + 1
                
                if dataEntries[1][i] == 77 and [2, 2.5, 11, 11.5, 12].count(float(dataEntries[2][i])) > 0:
                    dataEntries[1][i] = 66

         
        i = i + 1



    return dataEntries

    
def keyBoardEnter(dataEntries):

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

    
    #add to setting later (time before data enter)
    time.sleep(5)

    i = 0
    while i < len(dataEntries[1]):
    
        #TYPE IN CODE, MOVE TO $AMOUNT
        keyboard.type(str(dataEntries[1][i]))
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(time1)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        
        
        #TYPE IN $ AMOUNT, MOVE TO BUTTON
        keyboard.type(str(dataEntries[2][i]))
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
        if int(dataEntries[1][i]) == 68:
            keyboard.press(Key.enter)
            time.sleep(0.3)
            keyboard.release(Key.enter)

        elif int(dataEntries[1][i]) == 34 and int(dataEntries[2][i]) > 350 :
            keyboard.press(Key.enter)
            time.sleep(0.3)
            keyboard.release(Key.enter)

        elif int(dataEntries[1][i]) == 66 and int(dataEntries[2][i]) > 35 :
            keyboard.press(Key.enter)
            time.sleep(0.3)
            keyboard.release(Key.enter)
            
        elif int(dataEntries[1][i] == 20) and int(dataEntries[2][i]) > 300 :
            keyboard.press(Key.enter)
            time.sleep(0.3)
            keyboard.release(Key.enter)
            
        time.sleep(time2)
        i = i + 1    
        
    winsound.Beep(2000, 400)


def main():
    
    #set up window
    window = tk.Tk()
    window.title("Typer")
    window.geometry("800x800")
    lbl = tk.Label(window, text=" enter instructions here")
    lbl.grid(column=1,row=0)

    #font
    txt = scrolledtext.ScrolledText(window,width=40, height=20)
    txt.config(font=("courier", 15, "normal"))
    txt.grid(column=1, row=2)
    
    #button1
    btn = tk.Button(window, text="click me", command=lambda: buttonClick(txt.get("1.0", "end-1c")))
    btn.grid(column=1, row=1)

    
    window.mainloop()

if __name__  == "__main__":
    main()



