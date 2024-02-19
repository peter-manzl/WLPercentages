# -*- coding: utf-8 -*-
"""
                MyWLGUI.py
@author:        Peter Manzl, <peter.manzl@outlook.com>
description:    A minimalistic python program using a tkinter GUI to keep track
                of the weights at the gym.  
Licence:        Use is permitted under the MIT licence: 
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 
 
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 


"""

#%% 

import tkinter as tk
from PIL import ImageTk, Image
# import os
from numpy import array, ceil, loadtxt, savetxt

# import numpy as np
def toString(myFloat): 
    if myFloat // 1 == myFloat: 
        return str(int(myFloat))
    else: 
        return str(myFloat)

class WLPercWindow(): 
    def __init__(self): 
        self.result_labels = []
        self.maxEntriesPerRow = 3
        self.numTopGrid = 7
        try: 
            self.RMLIst, self.percentageList = self.readData()
        except: 
            self.RMList = []
            self.percentageList = []
    
    def ListToString(self, myList): 
        myStr = ''    
        for perc in myList: 
            myStr += toString(perc) + ','
        mySTr = myStr[:-1]
        return mySTr
    
    def StringToList(self, myString): 
        myString = myString.split('#')[0] # cut away comment
        myList = []
        for data in myString.split(','): 
            myList += [float(data)]
        return myList
    
    def readData(self, dataFile="lastData.txt"):
        with open(dataFile, "r") as file:
        	# Writing data to a file
            myLines = file.readlines()
            
            rmList = self.StringToList(myLines[1])
            percentageList = self.StringToList(myLines[2])
            file.close() # to change file access modes 
        self.RMList = rmList
        self.percentageList = percentageList
        return 
    
    
    def saveData(self, dataFile="lastData.txt"): 
        with open(dataFile, "w") as file:
            # Writing data to a file
            file.write("Temporary data for Weightlifting percentages\n")
            strRMsList = self.ListToString(self.RMList)
            strPercentageList = self.ListToString(self.percentageList)
            
            file.writelines(strRMsList + ' # kg\n')
            file.writelines(strPercentageList + ' # %\n')
            file.close() # to change file access modes
        return
        
    def calculate_percentage(self): 
        # try:
            value = entry1RM.get()
            if ',' in value: 
                RMList = []
                for val in value.split(','): 
                    if len(val) > 1: 
                        RMList += [float(val)]
            else: 
                RMList = [float(value)]
                
            Percentages = entryPerc.get()
            if ',' in Percentages: 
                percentageList = []
                for val in Percentages.split(','): 
                    if len(val) > 1: 
                        percentageList += [float(val)]
            else: 
                percentageList = [float(Percentages)]
            
            self.percentageList = percentageList
            self.RMList = RMList
            # percentageList = np.array([0.70, 0.76, 0.82, 0.80])
            for label in self.result_labels: 
                label.after(50, label.destroy())
            
            self.result_labels = []
            for j, value in enumerate(RMList): 
                valuesPercentage = value * array(percentageList)/100
                # percentage = number * 0.10  # Calculate 10% of the input number
                if value // 1 == value: 
                    valStr = str(int(value))
                else: 
                    valStr = str(value)
                strShow = "Athlete " + str(j+1) + " ({}kg):\n".format(valStr)
                for i, val in enumerate(valuesPercentage): 
                    strShow += '{}%    -  '.format(percentageList[i])
                    strShow += (str(round_WL(val)) + 'kg\n').rjust(10)
                self.result_labels += [tk.Label(root, text="")]
                # self.result_labels[-1].pack()
                row = self.numTopGrid + j // self.maxEntriesPerRow
                col = j % self.maxEntriesPerRow
                if col == 0 and len(RMList)% 3 == 1 and j == (len(RMList) -1): 
                    col += 1
                self.result_labels[-1].grid(row=row, column=col)
                self.result_labels[-1].config(text=strShow, font=("Arial", 18))
        # except ValueError:
        #     print("Please enter a valid number")
        
def round_WL(value): 
    # value = value - value % 0.5 # round down to next 0.5kg step
    value = ceil(value*2)/2 # round up to next 0.5 kg step
    return value 

if __name__ == '__main__':
    iColumnMiddle = 1
    my_WLWindow = WLPercWindow()
    try: 
        my_WLWindow.readData()
    except: 
        print('no Data saved (yet)')
        my_WLWindow.RMList = []
        my_WLWindow.percentageList = []
    root = tk.Tk()
    root.title("WL % Calculator")
    root.geometry('+200+200')
    # root.geometry('520x300+50+50')
    try: 
        image = Image.open("Logo.png").resize((300, 300))
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=image)
        image_label.grid(column = iColumnMiddle)
        root.iconphoto(False, image)
    except: 
        
        imageMissingLabel = tk.Label(root, text="<Logo missing. ", font=("Arial", 25))
        imageMissingLabel.grid(column = iColumnMiddle)
        
        
    
    
    
    label = tk.Label(root, text="Enter 1RM:", font=("Arial", 18))
    label.grid(column = iColumnMiddle)
    
    entry1RM = tk.Entry(root, font=("Arial", 15), textvariable=tk.StringVar(value=my_WLWindow.ListToString(my_WLWindow.RMList)))
    entry1RM.grid(column = iColumnMiddle)
    
    labelPerc = tk.Label(root, text="Enter Percentages,\n e.g. '70, 80, 90'", font=("Arial", 18))
    labelPerc.grid(column = iColumnMiddle)
    
    entryPerc = tk.Entry(root, font=("Arial", 15), textvariable=tk.StringVar(value=my_WLWindow.ListToString(my_WLWindow.percentageList)))
    entryPerc.grid(column = iColumnMiddle)
    
    
    
    calculate_button = tk.Button(root, text="Calculate", command=my_WLWindow.calculate_percentage, font=("Arial", 15))
    calculate_button.grid(column = iColumnMiddle)
    def hitReturn(myWindow): 
        my_WLWindow.calculate_percentage()
    root.bind('<Return>', hitReturn)
    # root.attributes('-topmost',True)
    root.mainloop()
    
    my_WLWindow.saveData()