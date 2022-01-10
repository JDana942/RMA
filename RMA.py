#!/usr/bin/env python3
# RMA version 00.01

from os import times
from tkinter.constants import BOTTOM, CENTER, COMMAND, E, END, LEFT, NE, NW, RIDGE, RIGHT, S, SE, SW, TOP, W
import tkinter as tk
import mysql.connector
from time import sleep
import mysql
from datetime import date, datetime
import csv

# Creating the App window
window = tk.Tk()
window.title("RMA _ Login")
window.geometry("500x300")
window.minsize(500,300)

# Database login credentials
dbField = "rma"
usernameField = tk.Entry()
passwordField = tk.Entry(show="*")
homePhoto = tk.PhotoImage(file= '\\Users\JohnDana\Downloads\homeButton.png')
tempdevice = ['Select an Option']
reasonList = ['Select an Option']

# Main function selection screen
def homeMenu():
    clearWindow()
    window.title("RMA _ Home")
    window.update()
    window.minsize(500,300)
    addButton = tk.Button(text="Add Device",font = ('Arial', 16),height=1, width=12,command=addMenu)
    searchButton = tk.Button(text="Search Device",font = ('Arial', 16),height=1, width=12,command=searchMenu)
    editButton = tk.Button(text="Edit Device",font = ('Arial', 16),height=1, width=12,command=editDevice)
    reportButton = tk.Button(text="Reports",font = ('Arial', 16),height=1, width=12,command=generateReports)
    addButton.grid(row = 0,column=0,padx=20,pady=20,sticky=SE)
    searchButton.grid(row = 0,column=1,padx=20,pady=20,sticky=SW)
    editButton.grid(row = 1,column=0,padx=20,pady=20,sticky=NE)
    reportButton.grid(row = 1,column=1,padx=20,pady=20,sticky=NW)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    tempdevice[0] = 'Select an Option'

# Used for adding devices into the RMA system
def addMenu():

    # Gets the Device option and reads the database reasons table for the issues related to the device. 
    # Then passes it to the OptionMenu for the reason list.
    def getOption(self):
        
        deviceTypeString = deviceType.get()
        sqlQuery = 'SELECT `'+ deviceTypeString +'` FROM reasons'
        
        try:
            curA.execute(sqlQuery)
            tempreasonList = curA.fetchall()
            tempreasonList = str(tempreasonList)
            tempreasonList = tempreasonList.replace(",)", "").replace(" (","").replace('"', "").replace("'", "").replace("[","").replace("]","").replace("(","").replace(";","").replace("None", "")
            tempreasonList = tempreasonList.replace(",", "\n").splitlines()
            fparsetempList = list(filter(None, tempreasonList))

            reasonList.clear()         
            
            for i in range(len(fparsetempList)):
                reasonList.append(fparsetempList[i])

            for i in range(len(deviceMenuOptions)):
                if deviceTypeString == deviceMenuOptions[i]:
                    tempdevice[0] = deviceMenuOptions[i]
                else:
                    pass
        
        except mysql.connector.errors.ProgrammingError:
            print("Failed to Query")
  
        addMenu()
        
    def addDevice():
        
        # Takes the device list string and forms a list seperated by comma or nl.
        deviceListAdd = deviceList.get("1.0",END)
        deviceListAdd = deviceListAdd.replace(" ", "").replace(";","")
        parsedeviceList = deviceListAdd.replace(",", "\n").splitlines()
        fparsedeviceList = list(filter(None, parsedeviceList))
        
        clearWindow()
        window.minsize(500,300)
        addPrompt = tk.Label(text="Adding Devices to Database...",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
        window.update()
        sleep(1.5)

        # Reads the optionMenu selections in string format
        deviceInput = deviceType.get()
        reasonInput = reasonFieldType.get()
        locationInput = locationType.get()
        ownerInput = ownershipType.get()
        statusInput = statusType.get()
        dateInput = str(date.today())
        dateInput = dateInput.replace(",","-")
        print(dateInput)

        values = []
        
        # Used for adding new entries into the database
        # Currently the system will add multiple entries for the same device to track history ---- Subject to future changes ----
        
        try: 
            sqlQuery = "INSERT INTO rmadata (ID, type, location, owner, reason, status, date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            for i in range(len(fparsedeviceList)):
                tempData = (fparsedeviceList[i],deviceInput,locationInput,ownerInput,reasonInput,statusInput,dateInput)
                values.append(tempData)
            curA.executemany(sqlQuery,values)
             
        except:
            clearWindow()
            window.minsize(500,300)
            addPrompt = tk.Label(text="Failed to Add to Database",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
            window.update()
            sleep(1.5)

        finally:
            rmadb.commit()
            clearWindow()
            successPrompt = tk.Label(text="Success",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
            window.update()
            sleep(1.5)
            homeMenu()
        

    clearWindow()
    curA = rmadb.cursor()
    window.title("RMA _ Add Device")
    window.minsize(1000,400)
    homeButton = tk.Button(image=homePhoto, height=40, width=40,command=homeMenu).place(relx="0", rely="0")
    deviceType = tk.StringVar(window)
    deviceType.set(tempdevice[0])
    deviceMenuOptions = [
        "Tag",
        "Gateway",
        "Relay",
        "Evac Tag",
        "Checkin Station",
        "Turnstile Unit"
    ]
    deviceMenu = tk.OptionMenu(window, deviceType ,*deviceMenuOptions,command=getOption)
    deviceMenu.place(relx="0.15",rely="0.2",anchor=CENTER)

    reasonFieldType = tk.StringVar(window)
    reasonFieldType.set("Select an Option")
    reason = tk.OptionMenu(window, reasonFieldType, *reasonList)
    reason.place(relx="0.35",rely="0.2",anchor=CENTER)    
    deviceReasonPrompt = tk.Label(text="Select Reason:",font=("Arial",12)).place(relx="0.35",rely="0.1",anchor=CENTER)
    
    locationType = tk.StringVar(window)
    locationType.set("Select an Option")
    locationMenuOptions = [
        "Norwalk",
        "East Hartford",
        "Triumph"
    ]
    locationMenu = tk.OptionMenu(window, locationType ,*locationMenuOptions)
    locationMenu.place(relx="0.15",rely="0.6",anchor=CENTER)
    locationPrompt = tk.Label(text="Set Location",font=("Arial",12)).place(relx="0.15",rely="0.5",anchor=CENTER)
    
    ownershipType = tk.StringVar(window)
    ownershipType.set("Select an Option")
    ownershipMenuOptions = [
        "Triax",
        "United Rentals",
        "Gilbane"
    ]
    ownershipMenu = tk.OptionMenu(window, ownershipType ,*ownershipMenuOptions)
    ownershipMenu.place(relx="0.35",rely="0.6",anchor=CENTER)
    ownershipPrompt = tk.Label(text="Set Ownership",font=("Arial",12)).place(relx="0.35",rely="0.5",anchor=CENTER)
    
    statusType = tk.StringVar(window)
    statusType.set("Select an Option")
    statusMenuOptions = [
        "RMA",
        "Serviced",
        "Retired"
    ]
    statusMenu = tk.OptionMenu(window, statusType ,*statusMenuOptions)
    statusMenu.place(relx="0.55",rely="0.2",anchor=CENTER)
    statusPrompt = tk.Label(text="Set Status",font=("Arial",12)).place(relx="0.55",rely="0.1",anchor=CENTER)

    deviceTypePrompt = tk.Label(text="Device Type",font=("Arial",12)).place(relx="0.15",rely="0.1",anchor=CENTER)
    
    deviceList = tk.Text()
    deviceList.place(width=160,height=200,relx="0.7",rely="0.15")
    deviceListPrompt = tk.Label(text="Device List:",font=("Arial",12)).place(relx="0.78",rely="0.1",anchor=CENTER)
    deviceListNote = tk.Label(text="Input Full Serial:\n(CCP0301-00004488)",font=("Arial",8)).place(relx="0.78",rely="0.7",anchor=CENTER)
    addButton = tk.Button(foreground = 'blue',font = ('calibri', 14, 'bold'),text="ADD", command=addDevice)
    addButton.place(relx="0.94",rely="0.88")
    

# Used for looking up device info
# Possible Future Update (5 or less devices will be output to the window)
def searchMenu():

    def searchDevice():
        searchList = searchBox.get("1.0",END)
        searchList = searchList.replace(" ", "").replace(";","")
        parseSearchList = searchList.replace(",", "\n").splitlines()
        fparseSearchList = list(filter(None, parseSearchList))

        searchReturnList = []
        notFoundList = []

        try: 
            sqlQuery = 'SELECT * FROM `rmadata` WHERE ID = %s'
            for i in range(len(fparseSearchList)):
                value = (fparseSearchList[i], )
                curA.execute(sqlQuery,value)
                tempData = curA.fetchall()
                
                if tempData == []:
                    notFoundList.append(value[0])
                
                else:
                    searchReturnList.append(tempData)

            if notFoundList != []:
                print("The Following Devices Were Not Found:")
                print(notFoundList)

            line1 = searchReturnList[0]
            print(line1[0])
            timeStamp = datetime.now()
            filename = "searchResults-"+str(timeStamp.year)+"-"+str(timeStamp.month)+"-"+str(timeStamp.day)+" "+str(timeStamp.hour)+"."+str(timeStamp.minute)+".csv"
            with open(filename, 'w') as searchFile:
                w = csv.writer(searchFile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
                #w.writerows(notFoundList[0])
                w.writerows(searchReturnList)
            
             
        except NotImplementedError:
            clearWindow()
            window.minsize(500,300)
            addPrompt = tk.Label(text="Failed to Query",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
            window.update()
            sleep(1.5)

        finally:
            rmadb.commit()
            clearWindow()
            successPrompt = tk.Label(text="Search Success\nFile Downloading",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
            window.update()
            sleep(1.5)
            homeMenu()

    clearWindow()
    window.title("RMA _ Search Device")
    window.minsize(600,350)

    curA = rmadb.cursor()

    homeButton = tk.Button(image=homePhoto, height=40, width=40,command=homeMenu).place(relx="0", rely="0")
    searchNote = tk.Label(text="Input Full Serials \n ex..(CCP0301-00004488)",font=("Arial",12)).place(relx="0.5",rely="0.1",anchor=CENTER)
    searchBox = tk.Text()
    searchBox.place(width=180,height=220, relx="0.5", rely="0.5",anchor=CENTER)
    searchButton = tk.Button(foreground = 'blue',font = ('calibri', 14, 'bold'),text="Search", command=searchDevice)
    searchButton.place(relx="0.92",rely="0.9",anchor=CENTER)
    outputNote = tk.Label(text="This function will export the data as\na .csv in the application Folder", font=("Arial",8)).place(relx="0.16",rely="0.92", anchor=CENTER)
    

# Used for Editing Device information
def editDevice():
    clearWindow()
    window.title("RMA _ Edit Device")
    window.minsize(1000,400)
    homeButton = tk.Button(image=homePhoto, height=40, width=40,command=homeMenu).place(relx="0", rely="0")

# Used to Generate Reports from the database data
def generateReports():
    clearWindow()
    window.title("RMA _ Reports")
    window.minsize(1000,400)
    homeButton = tk.Button(image=homePhoto, height=40, width=40,command=homeMenu).place(relx="0", rely="0")


# Clears the widgets from the display "Cant use destroy due to global wigets (username / password / ...ect)"
def clearWindow():
    for widget in window.winfo_children():
        widget.place_forget()
        widget.pack_forget()
        widget.grid_forget()
    window.update()
    return

# Checks the login credentials
def passCheck():
    inputusername = usernameField.get()
    inputpassword = passwordField.get()
    clearWindow()
    passPrompt = tk.Label(text="Connecting to Database...",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
    window.update()
    sleep(1.5)
    try:
        global rmadb 
        rmadb = mysql.connector.connect(user=inputusername, password =inputpassword, database = dbField)
        homeMenu()
    except mysql.connector.Error:
        clearWindow()
        dbrejectPrompt = tk.Label(text="Connection Failed",font=("Arial",20)).place(relx="0.5",rely="0.5",anchor=CENTER)
        window.update()
        sleep(1.5)
        clearWindow()
        main()

# Main Login Screen
def main():
    heading = tk.Label(text="RMA Mannagment System",font=("Arial",20)).pack(side=TOP)
    usernamePrompt= tk.Label(text="Username:",font=("Arial",18)).place(relx="0.37",rely="0.4",anchor=CENTER)
    usernameField.place(relx="0.62",rely="0.4",anchor=CENTER)
    passwordPromp = tk.Label(text="Password:",font=("Arial",18)).place(relx="0.37",rely="0.6",anchor=CENTER)
    passwordField.place(relx="0.62",rely="0.6",anchor=CENTER)
    enterButton_main = tk.Button(foreground = 'blue',font = ('calibri', 14, 'bold'),text="Login",
                                 command=passCheck)
    enterButton_main.place(relx="0.85",rely="0.84")   

if __name__ == "__main__":
    main()


window.mainloop()